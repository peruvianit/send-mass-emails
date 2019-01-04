

import yaml
import re


class RegularExpressionHelper:
    def __init__(self):
        self.code = yaml.load(open('regularExpression.yaml'))


    def match(self, name_regular_expression, content):
        result_match = False
        try:
            regex = self.code['regular'][name_regular_expression]
        except KeyError:
            raise KeyError("Problem find Key : {}".format(name_regular_expression))

        if re.search(regex, content):
            result_match = True
        
        return result_match