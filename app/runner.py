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


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


LOG_FILENAME = '../log/send-mass-email.log'
handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=10485760, backupCount=5)
logger.addHandler(handler)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

config = Config()


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


def _move_file_to_processed_directory(name_file_working):
    shutil.move("../data/working/{}".format(name_file_working), "../data/processed/{}".format(name_file_working.replace(".tmp",".csv")))


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
            for row in csv_reader:
                if line_count > 0:
                    client = _get_client(row)
                    client_dict = client.to_dict()
                    try:
                        sender.sendMessage(client)
                    except smtplib.SMTPRecipientsRefused as rR:
                        logger.error(rR)
                    except IOError as e:
                        logger.error(e)
                        sys.exit(1) # Not found template
                    except:
                        logger.error("Problem sending email for client : {} ".format(client.to_string()))
                        value = 'KO'
                    else:
                        logger.debug('mail to {} <{}> successfully send success'.format(client.contact, client.email)) 
                        value = 'OK'

                    client_dict['result'] = value
                    writer.writerow(client_dict)
                line_count += 1
                
            logger.info(f'Processed {line_count - 1} mails.')

        _move_file_to_processed_directory(name_file_working)


if __name__ == '__main__':
    logger.info("Start application")
    templateHelper = TemplateHelper("campaign-01")

    _read_and_process_data(templateHelper)
    
    logger.info("End application")