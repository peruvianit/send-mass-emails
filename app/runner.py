# Sending Email - massive
'''

'''
import sys
import csv
import smtplib
import shutil
import logging
import argparse
from logging.handlers import RotatingFileHandler

from email.message import EmailMessage
import datetime

from model.client import Client
from config.config import Config
from send.sender import Sender
from helper.templateHelper import TemplateHelper
from helper.fileHelper import FileHelper
from helper.applicationHelper import *
from helper.regularExpressionHelper import RegularExpressionHelper
from grafic.progressBar import ProgressBar
from enumApp.stateClient import StateClient
from exception.sendMailException import SendMailException
from helper.cleanFileHelper import CleanFileHelper

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


LOG_FILENAME = '../log/send-mass-email.log'
handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=10485760, backupCount=5)
logger.addHandler(handler)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

config = Config()

p = ProgressBar('==> send email...')

def _get_client(row):
    """ 
        Creating Client with the row of the file csv 
    """

    id = row[0]
    ruc = row[1]
    enterprise = row[2]
    contact = row[3]
    phone = row[4]
    email = row[5]
    state = row[6]

    client = Client(id,ruc,enterprise,contact,phone,email,state)
    return client


def _create_name_file_working(file_name):
    date_now =f"{datetime.datetime.now():%Y%m%d}"
    time_now =f"{datetime.datetime.now():%H%M}"

    return file_name.replace(".csv","_{}_{}.tmp".format(date_now,time_now))


def _move_file_to_processed_directory(name_file_working, name_template):
    shutil.move("../data/working/{}".format(name_file_working), "../data/processed/{name_template}_{filename}".format(name_template=name_template, filename=name_file_working.replace(".tmp",".csv")))


def _get_lines_csv_reader(name_file_data_email):
    with open("../data/input/{}".format(name_file_data_email)) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for idx, row in enumerate(csv_reader):
            pass

    return idx


def _read_and_process_data(templateHelper):
    """
        Reading file csv, before an file with success
    """
    sender = Sender(config, templateHelper)

    name_file_data_email = config.name_file_data_email

    with open("../data/input/{}".format(name_file_data_email)) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')

        line_count = 0

        name_file_working = _create_name_file_working(name_file_data_email)

        with open('../data/working/{}'.format(name_file_working), mode='w', newline='') as csv_file_writer:
            writer = csv.DictWriter(csv_file_writer, fieldnames=Client.columns_name(), delimiter =";")

            writer.writeheader()
            client_dict = {}
            value = ''
            numRows = _get_lines_csv_reader(name_file_data_email)
            for row in csv_reader:
                if line_count > 0:
                    client = _get_client(row)

                    if client.state != StateClient.ACTIVE.value:
                        logger.debug('mail to {} <{}> not send but the state is {}'.format(client.contact, client.email, client.state))
                        value = '--'
                    else:
                        try:
                            sender.sendMessage(client)
                        except SendMailException as sEx:
                            logger.fatal(sEx)
                            raise
                        except smtplib.SMTPRecipientsRefused as rR:
                            logger.error(rR)
                            value = 'KO'
                        except IOError as e:
                            logger.error(e)
                            sys.exit(1) # Not found template
                        except:
                            logger.error("Problem sending email for client : {} ".format(client.to_string()))
                            value = 'KO'
                        else:
                            logger.debug('mail to {} <{}> successfully send success'.format(client.contact, client.email)) 
                            value = 'OK'

                    client_dict = client.to_dict()
                    client_dict['result'] = value
                    writer.writerow(client_dict)

                    p.calculateAndUpdate(line_count, numRows)
                line_count += 1
                
            logger.info(f'Processed {line_count - 1} mails.')

        _move_file_to_processed_directory(name_file_working, templateHelper.name_template)


def _getTemplate():
    print('Select an template :\n ')
    fileHelper = FileHelper()

    directories = fileHelper.list_directories("../templates/")

    for idx, directory in enumerate(directories):
        print('{}) {}'.format(idx +1 , directory))

    print('\nwrite [exit] for exit application\n')

    while True:
        opt=input('Select an number of the list : ')    

        if (opt.upper() == 'EXIT'):
            return None
        elif (not opt.isdigit()):
            continue            
        else:
            if (int(opt) >= 1 and int(opt) <= len(directories) ):
                return directories[int(opt)-1]
            else:                
                continue


def _finish():
     logger.info("End application success")


def _synchronize():
    """
        Reading file csv, for synchronizer emails
    """
    sender = Sender(config)

    name_file_data_email = config.name_file_data_email

    with open("../data/input/{}".format(name_file_data_email)) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')

        line_count = 0

        name_file_working = _create_name_file_working(name_file_data_email)

        regularExpressionHelper = RegularExpressionHelper()

        with open('../data/input/{}'.format(name_file_working), mode='w', newline='') as csv_file_writer:
            writer = csv.DictWriter(csv_file_writer, fieldnames=Client.columns_name_synchronizer(), delimiter =";")

            writer.writeheader()
            client_dict = {}
            numRows = _get_lines_csv_reader(name_file_data_email)
            for row in csv_reader:
                if line_count > 0:
                    client = _get_client(row)

                    state = ''
                    if (regularExpressionHelper.match('email', client.email)):
                        if (sender.verify_email(client.email)):
                            state = StateClient.ACTIVE.value
                        else:
                            state = StateClient.WRONG.value
                    else:
                        state = StateClient.CORRUPT.value

                    client_dict = client.to_dict()
                    client_dict['state'] = state
                    writer.writerow(client_dict)

                    p.calculateAndUpdate(line_count, numRows)
                line_count += 1
                
            logger.info(f'Processed {line_count - 1} mails.')

    shutil.move('../data/input/{}'.format(name_file_data_email),'../data/input/{}'.format(name_file_working).replace(".tmp",".bck"))
    shutil.move('../data/input/{}'.format(name_file_working),"../data/input/{}".format(name_file_data_email))
        

def _clear():
    logger.info("Start cleannig olds files")
    cleanFileHelper = CleanFileHelper()

    number_days_old_passed = config.number_days_old_passed

    if not number_days_old_passed.isdigit():
        raise SendMailException("The property NUMBER_DAYS_OLD_PASSED into file config.ini not is a number : [{}]".format(number_days_old_passed))

    directories_storages = config.directories_storages.split("|")
    files_deleted = cleanFileHelper.cleanup(int(number_days_old_passed), directories_storages, 'send-mass-email')

    for file in files_deleted[1]:
        logger.info("file deleted : {}".format(file))

    logger.info("finish cleannig number [{}] olds files".format(files_deleted[0]))


if __name__ == '__main__':
    logger.info("Start application")

    parser = argparse.ArgumentParser( prog = "send-mass-emails", description = "Application sending mass email with data into file csv")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-s","--sync", help = "Synchronize emails to verify if they are valid", action = "store_true")
    group.add_argument("-c","--clear", help = "Clean all unusuable files", action = "store_true")
    parser.add_argument("-v","--version", action='version', version='%(prog)s 1.0.0')

    args = parser.parse_args()

    if args.sync:
        _synchronize()
        print('\nSynchronization completed successfully')
    elif args.clear:
        try:
            _clear()
            print('\ncleaning completed successfully')
        except SendMailException as sEx:
            logger.fatal(sEx)
            error_application(sEx)
    else:
        print(wellcome())
        name_template = _getTemplate()

        if (not name_template == None):
            try:
                templateHelper = TemplateHelper(name_template)
                _read_and_process_data(templateHelper)
                print('\nSending emails successfully completed')
            except SendMailException as sEx:
                logger.fatal(sEx)
                error_application(sEx)
            

        _finish()
   