# coding: utf-8

'''
Run tests on cole's '/collect' endpoint.
'''

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

from typing import Optional, Callable, Dict

from datetime import datetime, date, timedelta, timezone
import requests
import uuid

from tester.data import TestUsers


# -----------------------------------------------------------------------------
# Constants & Variables
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# Test Helpers
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


def _run_test(print_fn: Callable,
              url: str,
              params: Dict[str, str],
              day: date) -> bool:
    '''
    Calls URL w/ params, prints results, and returns pass/fail.
    '''
    print_fn()
    print_fn("─" * 5)
    print_fn("  params:", params)
    success = True

    if params.get('d', None):
        timestamp = datetime.fromtimestamp(params['d'], tz=timezone.utc)
        print_fn("    day:", day.isoformat())
        print_fn("    dt: ", timestamp.isoformat())
        if timestamp.date() != day:
            print_fn("    [FAIL]: Timstamp is incorrect for day!")
            success = False

    response = requests.get(url, params=params)
    print_fn(" ", ("[ OK ]" if response.ok else "[FAIL]"), "result:")
    success = success or response.ok

    print_fn("    status:", response.status_code, response.reason)
    print_fn("    url:   ", response.url)
    print_fn("    text:  ", response.text)

    return success


def _test_no_time(print_fn: Callable,
                  url: str,
                  users: TestUsers) -> bool:
    '''
    Run tests for random users without optional timestamp.
    '''
    success = True

    # Use "Today's" explicit vistors for this test.
    day, count = users.visited_today()
    for _ in range(count):
        params = _params(users.uuid_random())
        success = success and _run_test(print_fn, url, params, day)
        if not success:
            break

    return success


def _test_with_time(print_fn: Callable,
                    url: str,
                    users: TestUsers) -> bool:
    '''
    Run tests for random users with optional timestamp.
    '''
    success = True
    utc_today = datetime.utcnow().date()

    # Don't include today - `_test_no_time()` does that.
    for day, count in users.visited_uniques(include_today=False):
        # Tested that my `users` dict is ok - Got confused by the `repeats` I
        # made that were 06-13. Remove this now as it's not future-proof
        # against whenever next it runs.
        #
        # if day == utc_today:
        #     print_fn("[FAIL]: `_test_with_time` should not be including any "
        #              "of today's date!")
        #     success = False
        #     break

        # Hit REST API with `count` users, random timestamps in `day`.
        for _ in range(count):
            timestamp = users.random_timestamp(day)
            params = _params(users.uuid_random(), timestamp)
            success = success and _run_test(print_fn, url, params, day)
            if not success:
                break
        if not success:
            break

    return success


def _test_repeats(print_fn: Callable,
                  url: str,
                  users: TestUsers) -> bool:
    '''
    Run tests for repeat users with optional timestamp.
    '''
    success = True

    # Each day has a list of tuples of (name, num visits).
    for day, guests in users.visited_repeats():
        for name, count in guests:
            for _ in range(count):
                # Hit REST API with this user's number of visits today
                # (randomize timestamps).
                timestamp = users.random_timestamp(day)
                params = _params(users.uuid_repeatable(name), timestamp)
                success = success and _run_test(print_fn, url, params, day)

                # Cascade out on failure.
                if not success:
                    break
            if not success:
                break
        if not success:
            break

    return success


# -----------------------------------------------------------------------------
# Pubilc API
# -----------------------------------------------------------------------------

def test(print_fn: Callable,
         url: str,
         users: TestUsers) -> bool:
    '''
    Calls '/collect' endpoint with valid and invalid values,
    checks return code.

    Depends on other tests to verify it has actually set values for dates/user
    visits.
    '''
    success = True
    url = url + '/collect'

    # ------------------------------
    # Set-Up
    # ------------------------------
    print_fn("─" * 40)
    print_fn("/collect")
    print_fn("  url:", url)

    # ------------------------------
    # Test: All Repeat Users
    # ------------------------------
    if success:
        print_fn()
        print_fn("─" * 20)
        print_fn("User List (Repeats): With Timestamps")
        success = _test_repeats(print_fn, url, users)

    # ------------------------------
    # Test: Today's Users w/o Timestamps
    # ------------------------------
    if success:
        print_fn("─" * 20)
        print_fn("Today's Users: No Timestamps")
        success = _test_no_time(print_fn, url, users)

    # ------------------------------
    # Test: All Unique Users
    # ------------------------------
    if success:
        print_fn()
        print_fn("─" * 20)
        print_fn("User List (Uniques): With Timestamps")
        success = _test_with_time(print_fn, url, users)

    # ------------------------------
    # Done.
    # ------------------------------
    print_fn()
    print_fn("─" * 40)
    print_fn("[ OK ]" if success else "[FAIL]")
    return success
