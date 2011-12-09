#!/usr/bin/python
from os import sys

try:
    from twango.management.templates import *
except ImportError:
    from management.templates import *

cli_strings = {}

cli_strings['options'] = """
   usage: twango-admin.py startproject (path to project) -- (extra options)

"""

cli_strings['intro'] = """
    ***************************
    *   Twango Project        *
    ***************************

    running this command sets up a new project with some defaults
    that we have found helpful as a starting point

"""


def main(args):
        
        if len(args) < 3:
                print cli_strings['intro']
                print cli_strings['options']
                return

        if sys.argv[1] == 'startproject':
                print cli_strings['intro']
                startproject(sys.argv[2])

if __name__ == "__main__":
        main(sys.argv)

