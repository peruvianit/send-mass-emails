

import os


class FileHelper:
    def __init__(self):
        pass

    def list_directories(self, path_directory):
        directories = []

        for filename in os.listdir(path_directory):
            if os.path.isdir("{path}{filename}".format(path=path_directory, filename=filename)):
                directories.append(filename)

        return directories