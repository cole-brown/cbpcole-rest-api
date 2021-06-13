#!/usr/bin/env python3
# coding: utf-8

'''
Run tests on cole.
'''

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

from typing import Any, Callable, TextIO

import argparse
import os
import sys

from tester import collect, daily, monthly
from tester.data import TestUsers


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

    def error(self, message: str):
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

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help=("Enable verbose test output."))

    parser.add_argument(
        '--url', '-u',
        type=str,
        default='http://localhost:8080',
        help=("Root URL of the 'cole' REST APIs."))

    parser.add_argument(
        '--skip-collect', '-s',
        action='store_true',
        help=("Skip the '/collect' endpoint "
              "(skip creating database entries)."))

    # ------------------------------
    # Parse Command Line Args
    # ------------------------------
    args = parser.parse_args()
    return args


def get_test_printer(verbose: bool) -> Callable:
    '''
    Returns a verbosity-obeying print function.

    Or, more exactly, returns either a function that prints, or a fuction that
    does nothing, depending on `verbose`.
    '''
    if verbose:
        def test_printer(*args: Any, **kwargs: Any) -> None:
            print(*args, **kwargs)
        return test_printer

    def test_ignorer(*args: Any, **kwargs: Any) -> None:
        pass
    return test_ignorer


# -----------------------------------test--------------------------------------
# --               Run Tests on 'CBPC of Logging End-users'.                 --
# -----------------------------------------------------------------------------

if __name__ == '__main__':
    # ------------------------------
    #  Parse command line.
    # ------------------------------
    args = _args()

    # ------------------------------
    # Create testing data.
    # ------------------------------
    verbose = args.verbose
    print_fn = get_test_printer(verbose)
    url = args.url
    skip_collect = args.skip_collect
    users = TestUsers()
    success = True

    # ------------------------------
    # Run tests.
    # ------------------------------

    # ---
    # /collect
    # ---
    try:
        # Don't run collect - want to debug or test only the reports without
        # changing the database records.
        if skip_collect:
            if verbose:
                print("─" * 40)
                print("/collect")
                print("  url:", url)
                print("─" * 20)
            print("[-skip!-]: '/collect' tests skipped as requested.")
            if verbose:
                print("─" * 40)

        elif not collect.test(print_fn, url, users):
            success = False
            if verbose:
                print()
                print("─" * 20)
            print("[FAILURE]: '/collect' tests failed.")
            if verbose:
                print("─" * 40)

    except Exception as error:
        success = False
        if verbose:
            print()
            print("─" * 20)
        print("[FAILURE]: '/collect' tests failed with exception:")
        print(error)
        raise

    # ---
    # /daily_uniques
    # ---
    try:
        if not success:
            pass
        elif not daily.test(print_fn, url, users):
            success = False
            if verbose:
                print()
                print("─" * 20)
            print("[FAILURE]: '/daily_uniques' tests failed.")
            if verbose:
                print("─" * 40)

    except Exception as error:
        success = False
        if verbose:
            print()
            print("─" * 20)
        print("[FAILURE]: '/daily_uniques' tests failed with exception:")
        print(error)
        raise

    # ---
    # /monthly_uniques
    # ---
    try:
        if not success:
            pass
        elif not monthly.test(print_fn, url, users):
            success = False
            if verbose:
                print()
                print("─" * 20)
            print("[FAILURE]: '/monthly_uniques' tests failed.")
            if verbose:
                print("─" * 40)

    except Exception as error:
        success = False
        if verbose:
            print()
            print("─" * 20)
        print("[FAILURE]: '/monthly_uniques' tests failed with exception:")
        print(error)
        raise

    # ------------------------------
    # Done: Final Success/Failure
    # ------------------------------
    if verbose:
        print()
        print("─" * 40)
    if success:
        print("[SUCCESS]: All tests passed!")
    else:
        print("[FAILURE]: Some tests did not pass!")
