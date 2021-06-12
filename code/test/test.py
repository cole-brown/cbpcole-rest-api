#!/usr/bin/env python3
# coding: utf-8

'''
Run tests on cole.
'''

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

from typing import Optional, Type, NewType, Dict, Tuple, TextIO

from datetime import date, datetime, time, timedelta
import argparse
import math
import os
import random
import sys


# -----------------------------------------------------------------------------
# Constants & Variables
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# Command Helpers
# -----------------------------------------------------------------------------

class HelpfulErrorParser(argparse.ArgumentParser):
    '''Print usage if an error happens during arg parsing.'''

    def line(self,
             length:  int,
             stream:  TextIO,
             padding: int = 0):
        '''
        A section separation line built from ASCII/Unicode box character(s).
        '''
        stream.write('─' * (length + padding) + '\n')

    def error(self, message):
        '''
        Print error, then also print usage.

        Default argparse of "print error only" is pretty unhelpful when you
        also need to know how to fix your error...
        '''
        try:
            size = os.get_terminal_size(sys.stderr.fileno())
            width = size.columns
        except OSError:
            width = 80

        # ---
        # Header
        # ---
        self.line(width, sys.stderr)
        error_title = 'Error!'
        error_title_width = 20
        error_fmt = f'{{error_title:^{error_title_width}}}\n'
        sys.stderr.write(error_fmt.format(error_title=error_title))
        self.line(error_title_width, sys.stderr)

        # ---
        # Error Message
        # ---
        sys.stderr.write('\n')
        sys.stderr.write(message + '\n')
        self.line(width, sys.stderr)
        sys.stderr.write('\n')

        # ---
        # Help Message
        # ---
        self.print_help()
        sys.exit(2)


# -----------------------------------------------------------------------------
# Code
# -----------------------------------------------------------------------------

def _args() -> argparse.Namespace:
    '''
    Create ArgumentParser, parse command args, and return the Namespace object.
    '''
    # ------------------------------
    # Make Parser & Args.
    # ------------------------------
    parser = HelpfulErrorParser(
        description="Run some tests against cole.")

    # TODO: Do I want to steal any of my test selection stuff from veredi's
    # test runner?
    #   - I think I just want to always run everything.

    # TODO: what args does test even need?
    # parser.add_argument("-f", "--format",
    #                     help=("Python datetime parsing format. See: "
    #                           "https://docs.python.org/3/library/"
    #                           "datetime.html#strftime-strptime-behavior"))

    # parser.add_argument("-m", "--min",
    #                     help=("Time string for minimum datetime "
    #                           "allowable as output (exclusive)."))
    # parser.add_argument("-x", "--max",
    #                     help=("Time string for maximum datetime "
    #                           "allowable as output (exclusive)."))
    # parser.add_argument("-y", "--yes",
    #                     help=("Auto-confirm your willingness to "
    #                           "possibly trash your repository."))

    # parser.add_argument("time",
    #                     help="Time string to parse and munge.")

    # ------------------------------
    # Parse Command Line Args
    # ------------------------------
    args = parser.parse_args()
    return args


# -----------------------------------test--------------------------------------
# --               Run Tests on 'CBPC of Logging End-users'.                 --
# -----------------------------------------------------------------------------

if __name__ == '__main__':
    # ------------------------------
    #  Parse command line.
    # ------------------------------
    args = _args()

    # ------------------------------
    # Run tests.
    # ------------------------------
    print("TODO: run tests.")
