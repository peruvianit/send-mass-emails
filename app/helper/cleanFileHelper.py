

import os
import sys
import time
import zipfile
import datetime

from helper.fileHelper import FileHelper

class CleanFileHelper:
    """Clean FileHelper"""
    def __init__(self):
        pass


    def remove(self, path):
        """
        Remove the file or directory
        """
        if os.path.isdir(path):
            try:
                os.rmdir(path)
            except OSError:
                print("Unable to remove folder: {}".format(path))
        else:
            try:
                if os.path.exists(path):
                    os.remove(path)
            except OSError:
                print("Unable to remove file: {}".format(path))


    def cleanup(self, number_of_days, directories, star_file_name):
        fileHelper = FileHelper()

        files_working = []
        for directory in directories:
            files_old = fileHelper.get_files_old(number_of_days, "../{}".format(directory), star_file_name)
            files_working += files_old

        date_now =f"{datetime.datetime.now():%Y%m%d}"
        time_now =f"{datetime.datetime.now():%H%M}"
        send_mass_emails_zip = zipfile.ZipFile('../storage/send_mass_email_{date_now}_{time_now}.zip'.format(date_now = date_now,time_now = time_now ), 'w')

        for file in files_working:
            send_mass_emails_zip.write(file, compress_type=zipfile.ZIP_DEFLATED)

        send_mass_emails_zip.close()

        for file in files_working:
                self.remove(file)

        return (len(files_old),files_working)
