#!/usr/bin/python3
#
# expression.py
#

class Expression:
    def __init__(self, str):
        self.variable, self.value = str.split('=')
        if self.value.startswith('"'):
            self.value = self.value[1:]
        if self.value.endswith('"'):
            self.value = self.value[:-1]

    def evaluate(self, context):
        return context[self.variable] == self.value
