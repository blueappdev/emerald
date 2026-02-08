#
# commandlib.py
#

import sys

class CommandLineTool:
    def __init__(self):
        self.applicationName = 'unknown'

    def warn(self, *args):
        print(*args, file=sys.stderr)

    def error(self, *args):
        self.warn(self.applicationName+':', *args)
        sys.exit(2)

    def processAllArguments(self, arguments):
        self.processArguments(arguments[1:])

    def processArguments(self, arguments):
        raise NotImplementedError

    def processCommandLine(self):
        try:
            self.processAllArguments(sys.argv)
        except BrokenPipeError:
            pass
        except KeyboardInterrupt:
            print('Interrupted ...')
            # 130 is the standard Unix exit code for a program
            # terminated by SIGINT (Ctrl-C): 128 + signal number 2.
            sys.exit(130)  




