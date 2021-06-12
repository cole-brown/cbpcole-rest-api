#!/usr/bin/env python3
# coding: utf-8

'''
Run cole (Cbpc (Clostra Backend Programming Challenge) Of Logging End-users).

Serves REST API on provided '--host'/'--port' parameters.
'''

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

from typing import Optional, Type, NewType, Dict, Tuple, TextIO

import argparse
import logging
import os
import sys

from cole import server


# -----------------------------------------------------------------------------
# Constants & Variables
# -----------------------------------------------------------------------------

LOG_NAME_DEFAULT = 'cole.server'
LOG_LEVEL_DEFAULT = logging.DEBUG


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
        description="Run cole REST API.")

    parser.add_argument("--host",
                        default='localhost',
                        help=("Host IP/name."))

    parser.add_argument("--port",
                        type=int,
                        default=80,
                        help=("Host port number."))

    # ------------------------------
    # Parse Command Line Args
    # ------------------------------
    args = parser.parse_args()
    return args


def make_logger(name: str, level: int) -> logging.Logger:
    '''
    Set up the logger.
    '''
    # Create formatter.
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Create handler
    handler = logging.StreamHandler()
    handler.setLevel(level)
    # handler.setFormatter(formatter)

    # Create logger.
    _logger = logging.getLogger(name)
    _logger.setLevel(level)
    _logger.addHandler(handler)

    return _logger

# -----------------------------------test--------------------------------------
# --               Run Tests on 'CBPC of Logging End-users'.                 --
# -----------------------------------------------------------------------------

if __name__ == '__main__':
    # ------------------------------
    # Set-Up
    # ------------------------------
    _logger = make_logger(LOG_NAME_DEFAULT,
                          LOG_LEVEL_DEFAULT)

    # ------------------------------
    # Parse command line.
    # ------------------------------
    args = _args()

    # ------------------------------
    # Run backend.
    # ------------------------------
    _logger.debug("Running server at: %s:%d", args.host, args.port)
    # server.run(host=args.host,
    #            port=args.port)
