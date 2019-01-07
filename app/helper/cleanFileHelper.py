

import os
import sys
import time

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
            
            for file in files_old:
                self.remove(file)

            files_working += files_old

        return (len(files_old),files_working)
