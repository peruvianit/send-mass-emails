# Sending Email - massive
'''

'''
import sys
import csv
import smtplib
import shutil
import logging
from logging.handlers import RotatingFileHandler

from email.message import EmailMessage
import datetime

from model.client import Client
from config.config import Config
from send.sender import Sender
from helper.templateHelper import TemplateHelper
from helper.fileHelper import FileHelper
from helper.applicationHelper import wellcome
from grafic.progressBar import ProgressBar


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

    ruc = row[0]
    enterprise = row[1]
    contact = row[2]
    phone = row[3]
    email = row[4]

    client = Client(ruc,enterprise,contact,phone,email)

    return client


def _create_name_file_working(file_name):
    date_now =f"{datetime.datetime.now():%Y%m%d}"
    time_now =f"{datetime.datetime.now():%H%M}"

    return file_name.replace(".csv","_{}_{}.tmp".format(date_now,time_now))


def _move_file_to_processed_directory(name_file_working, name_template):
    shutil.move("../data/working/{}".format(name_file_working), "../data/processed/{name_template}_{filename}".format(name_template=name_template, filename=name_file_working.replace(".tmp",".csv")))


def _read_and_process_data(templateHelper):
    """
        Reading file csv, before an file with success
    """
    sender  = Sender(config, templateHelper)

    name_file_data_email = config.name_file_data_email

    with open("../data/input/{}".format(name_file_data_email)) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')

        line_count = 0

        name_file_working = _create_name_file_working(name_file_data_email)

        with open('../data/working/{}'.format(name_file_working), mode='w', newline='') as csv_file_writer:
            writer = csv.DictWriter(csv_file_writer, fieldnames=Client.columns_name())

            writer.writeheader()
            
            client_dict = {}
            value = ''
            numRows = 3
            for row in csv_reader:
                if line_count > 0:
                    client = _get_client(row)
                    try:
                        sender.sendMessage(client)
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
    print("\n\n==> End application success")


if __name__ == '__main__':
    logger.info("Start application")

    print(wellcome())

    name_template = _getTemplate()

    if (not name_template == None):
        templateHelper = TemplateHelper(name_template)

        _read_and_process_data(templateHelper)
    
    _finish()
    logger.info("End application success")