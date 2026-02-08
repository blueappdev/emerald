#
# tablib.py
#

import sys
import libs.commandlib

class TabTool(libs.commandlib.CommandLineTool):
    def __init__(self):
        super().__init__()
        self.applicationName = 'tabtool'

    def recordFrom(self, str, sep='\t'):
        record = str.split(sep)
        return [self.strip(each) for each in record]

    def strip(self, str):
        str = str.strip()
        if str.startswith('"'):
            str = str[1:]
        if str.endswith('"'):
            str = str[:-1]
        return str




