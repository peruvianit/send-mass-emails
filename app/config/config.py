

import configparser


config = configparser.ConfigParser()
config.read("../config/config.ini")

class Config:
    def __init__(self):
        self.file_encoding = config['DEFAULT']['FILE_ENCODING']
        self.name_file_data_email = config['DEFAULT']['NAME_FILE_DATA_EMAIL']
        self.number_days_old_passed = config['DEFAULT']['NUMBER_DAYS_OLD_PASSED']
        self.directories_storages = config['DEFAULT']['DIRECTORIES_STORAGES']
        self.smtp_host = config['EMAIL']['SMTP_HOST']
        self.smtp_host_port = config['EMAIL']['SMTP_HOST_PORT']
        self.smtp_account_username = config['EMAIL']['SMTP_ACCOUNT_USERNAME']
        self.smtp_account_password = config['EMAIL']['SMPT_ACCOUNT_PASSWORD']
        self.smtp_account_from = config['EMAIL']['SMTP_ACCOUNT_FROM']