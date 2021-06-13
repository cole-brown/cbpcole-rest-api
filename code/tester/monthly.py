# coding: utf-8

'''
Run tests on cole's '/monthly_uniques' endpoint.
'''

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

from typing import Optional, Type, NewType, Dict, Tuple, TextIO

from datetime import date, datetime, time, timedelta
import requests


# -----------------------------------------------------------------------------
# Constants & Variables
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# Code
# -----------------------------------------------------------------------------

def _params(timestamp: date) -> Dict[str, str]:
    '''
    Generate a REST API call url from the base `url` and the arguments `id`
    and (optional) `unixtime`.
    '''
    params = { 'd': timestamp.isoformat() }

    return params


def _run_test(url: str,
              params: Dict[str, str]) -> bool:
    '''
    Calls URL w/ params, prints results, and returns pass/fail.
    '''
    response = requests.get(url, params=params)
    print()
    print("─" * 5)
    print("  params:", params)
    print(" ", ("[ OK ]" if response.ok else "[FAIL]"), "result:")
    print("    status:", response.status_code, response.reason)
    print("    url:   ", response.url)
    print("    text:  ", response.text)

    return response.ok


def _test_today(url: str) -> bool:
    '''
    Run tests on timestamp of today.
    '''
    success = True

    for _ in range(10):
        params = _params(datetime.utcnow().date())
        success = success and _run_test(url, params)
        # TODO: don't break after 1
        break
        if not success:
            break

    return success


def test(url: str) -> bool:
    '''
    Calls '/monthly_uniques' endpoint with valid and invalid values,
    checks return code.
    '''
    success = True
    url = url + '/monthly_uniques'

    # ------------------------------
    # Set-Up
    # ------------------------------
    try:
        print("─" * 40)
        print("/monthly_uniques")
        print("  url:", url)
        print("─" * 20)

        # ------------------------------
        # Actual Tests.
        # ------------------------------
        # Some without timestamps.
        print("Today")
        success = _test_today(url)

        # print()
        # print("─" * 20)
        # print("With Timestamps")

        # # Some with timestamps.
        # if success:
        #     success = _test_with_time(url)

        # TODO: some way of verifying that the count is correct.

    except:
        success = False

    # ------------------------------
    # Done.
    # ------------------------------
    print()
    print("─" * 40)
    print("[ OK ]" if success else "[FAIL]")
    return success
