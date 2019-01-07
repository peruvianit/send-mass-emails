

import os
import sys
import time

class FileHelper:
    def __init__(self):
        pass

    def list_directories(self, path_directory):
        directories = []

        for filename in os.listdir(path_directory):
            if os.path.isdir("{path}{filename}".format(path=path_directory, filename=filename)):
                directories.append(filename)

        return directories


    def get_files_old(self, number_of_days, path, star_file_name):
        files_old = []
        """
        Removes files from the passed in path that are older than or equal 
        to the number_of_days
        """
        time_in_secs = time.time() - (number_of_days * 24 * 60 * 60)
        for root, dirs, files in os.walk(path, topdown=False):
            for file_ in files:
                full_path = os.path.join(root, file_)
                stat = os.stat(full_path)
                
                if (stat.st_mtime <= time_in_secs and file_.upper().startswith(star_file_name.upper())):
                    files_old.append(full_path)

        return files_old