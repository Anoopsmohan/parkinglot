__author__ = 'anoop.sm'

import os


class ValidateArgument(object):
    VALID_EXTENTIONS = ['txt']

    def __init__(self, arg):
        self.arg = arg

    # Check file path is correct or not
    def validate_file_path(self):
        return os.path.isfile(self.arg)

    # Check file extension is correct or not
    def validate_extension(self):
        return self.arg.split('.')[-1].lower() in self.VALID_EXTENTIONS