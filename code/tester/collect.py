# coding: utf-8

'''
Run tests on cole's '/collect' endpoint.
'''

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

from typing import Optional, Type, NewType, Dict, Tuple, TextIO

from datetime import date, datetime, time, timedelta
import requests
import uuid


# -----------------------------------------------------------------------------
# Constants & Variables
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# Code
# -----------------------------------------------------------------------------

def _params(id: uuid.UUID,
            unixtime: Optional[int] = None) -> Dict[str, str]:
    '''
    Generate a REST API call url from the base `url` and the arguments `id`
    and (optional) `unixtime`.
    '''
    params = { 'cid': id.hex }

    if unixtime:
        params['d'] = unixtime

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


def _test_no_time(url: str) -> bool:
    '''
    Run tests without optional timestamp.
    '''
    success = True

    for _ in range(10):
        params = _params(uuid.uuid4())
        success = success and _run_test(url, params)
        if not success:
            break

    return success

def _test_with_time(url: str) -> bool:
    '''
    Run tests with optional timestamp.
    '''
    success = True

    for _ in range(10):
        timestamp = datetime.utcnow()
        delta = timedelta(hours=1)
        unixtime = int((timestamp - delta).timestamp())
        params = _params(uuid.uuid4(), unixtime)
        success = success and _run_test(url, params)
        if not success:
            break

    return success

def test(url: str) -> bool:
    '''
    Calls '/collect' endpoint with valid and invalid values,
    checks return code.
    '''
    success = True
    url = url + '/collect'

    # ------------------------------
    # Set-Up
    # ------------------------------
    try:
        print("─" * 40)
        print("/collect")
        print("  url:", url)
        print("─" * 20)

        # ------------------------------
        # Actual Tests.
        # ------------------------------
        # Some without timestamps.
        print("No Timestamps")
        success = _test_no_time(url)

        print()
        print("─" * 20)
        print("With Timestamps")

        # Some with timestamps.
        if success:
            success = _test_with_time(url)

        # TODO: Repeat customers?

    except:
        success = False

    # ------------------------------
    # Done.
    # ------------------------------
    print()
    print("─" * 40)
    print("[ OK ]" if success else "[FAIL]")
    return success
