# coding: utf-8

'''
Run tests on cole's '/daily_uniques' endpoint.
'''

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

from typing import Callable, Dict

from datetime import date
import requests

from tester.data import TestUsers


# -----------------------------------------------------------------------------
# Constants & Variables
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# Test Helpers
# -----------------------------------------------------------------------------

def _params(timestamp: date) -> Dict[str, str]:
    '''
    Generate a REST API call url from the base `url` and the arguments `id`
    and (optional) `unixtime`.
    '''
    params = { 'd': timestamp.isoformat() }

    return params


def _run_test(print_fn: Callable,
              url: str,
              params: Dict[str, str],
              expected: str) -> bool:
    '''
    Calls URL w/ params, prints results, and returns pass/fail.

    Compares the response's text field against `expected`.
    '''
    response = requests.get(url, params=params)
    print_fn()
    print_fn("─" * 5)
    print_fn("  params:", params)
    print_fn(" ", ("[ OK ]" if response.ok else "[FAIL]"), "result:")
    print_fn("    status:       ", response.status_code, response.reason)
    print_fn("    url:          ", response.url)
    print_fn("    text:         ", "'" + response.text + "'")

    # Valid HTTP response? Check for expected output.
    if response.ok:
        if expected != response.text:
            print_fn("      != expected:", "'" + expected + "'")
            return False

    # This represents success now that we're here - failed earlier on
    # unexpected output if appropriate.
    return response.ok


def _test_date(print_fn: Callable,
               url: str,
               day: date,
               users: TestUsers) -> bool:
    '''
    Run tests on `day`'s users.
    '''
    return _run_test(print_fn,
                     url,
                     _params(day),
                     str(users.expected(day)))


# -----------------------------------------------------------------------------
# Pubilc API
# -----------------------------------------------------------------------------

def test(print_fn: Callable,
         url: str,
         users: TestUsers) -> bool:
    '''
    Calls '/daily_uniques' endpoint with valid and invalid values,
    checks return code.
    '''
    success = True
    url = url + '/daily_uniques'

    # ------------------------------
    # Set-Up
    # ------------------------------
    print_fn("─" * 40)
    print_fn("/daily_uniques")
    print_fn("  url:", url)
    print_fn("─" * 20)

    # ------------------------------
    # Test each date we have in `users'.
    # ------------------------------
    for day in users.dates_of_interest():
        success = _test_date(print_fn,
                             url,
                             day,
                             users)
        if not success:
            break

    # ------------------------------
    # Done.
    # ------------------------------
    print_fn()
    print_fn("─" * 40)
    print_fn("[ OK ]" if success else "[FAIL]")
    return success
