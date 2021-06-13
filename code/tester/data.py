# coding: utf-8

'''
Testing helper for creating/verifying test data.
'''

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

from typing import Optional, Union, Tuple, List

from datetime import datetime, date, timedelta, timezone
import uuid
import random


# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# Code
# -----------------------------------------------------------------------------

class TestUsers:
    '''
    Contains dict of dates->number-of-unique-users.

    Helpful functions for dealing with/reasoning about these users and dates.
    '''

    _UUID_NAMESPACE = uuid.uuid5(uuid.UUID(int=0), 'cole.tester.data')
    '''
    The 'namespace' for our UUIDs will be static so we can
    reproducably generate (the same) UUIDs for testing purposes.
    '''

    # -------------------------------------------------------------------------
    # Initialization
    # -------------------------------------------------------------------------

    def __init__(self) -> None:
        self.repeats = {
            date(2021,  5, 11): [
                ("alice", 5),
                ("bob", 5),
                ("charlie", 5),
            ],

            date(2021,  6, 11): [
                ("alice", 3),
                ("bob", 3),
                ("charlie", 11),
            ],
        }

        # Make sure we have some explicitly zero user days.
        self.users = {
            # Outside 60 day window, which doesn't matter, currently. They
            # still get recorded/reported.
            # [2021-02, 2021-03]: 2 total
            date(2021,  2,  1):  1,
            date(2021,  3,  1):  1,

            # An entire month with 0 users.
            date(2021,  4,  1):  0,  # NO USERS!
            # AND NO USERS IN BETWEEN!
            date(2021,  4, 30):  0,  # NO USERS!

            # 2021-05:           20 total
            #          [01, 05]:  5
            #           10     : 10
            #          [15, 31]:  5
            date(2021,  5,  1):  1,
            date(2021,  5,  2):  1,
            date(2021,  5,  3):  1,
            date(2021,  5,  4):  1,
            date(2021,  5,  5):  1,
            date(2021,  5, 10): 10,
            date(2021,  5, 15):  1,
            date(2021,  5, 20):  1,
            date(2021,  5, 22):  0,  # NO USERS!
            date(2021,  5, 25):  1,
            date(2021,  5, 30):  1,
            date(2021,  5, 31):  1,

            # 2021-06:           70 total
            #          [01, 12]: 50
            #          [15, 30]: 20
            date(2021,  6,  1): 10,
            date(2021,  6,  5): 10,
            date(2021,  6,  7):  0,  # NO USERS!
            date(2021,  6, 10): 10,
            date(2021,  6, 12): 20,
            date(2021,  6, 15):  5,
            date(2021,  6, 20):  5,
            date(2021,  6, 25):  5,
            date(2021,  6, 30):  5,
        }

        self.todays = (datetime.utcnow().date(), 42)

    # -------------------------------------------------------------------------
    # Iterate Dates/Users
    # -------------------------------------------------------------------------

    def visited_today(self) -> Tuple[date, int]:
        '''
        Returns the tuple of (utc-today, num-uniques).
        '''
        return self.todays

    def visited_uniques(self, include_today: bool = False) -> Tuple[date, int]:
        '''
        Generator for returning `self.users` dictionary items.

        Each item is: visit-date -> num-unique-users-visited

        If `include_today` is True, also includes `self.todays`.
        '''
        for each in self.users.items():
            yield each

        # Also require some users in UTC-today?
        if include_today:
            yield self.todays

    def visited_repeats(self) -> Tuple[date, List[Tuple[str, int]]]:
        '''
        Generator for returning `self.repeats` dictionary items.

        Each item is: vist-date -> [ ('user-name-0', num-visits-0), ... ]
        '''
        for each in self.repeats.items():
            yield each

    def dates_of_interest(self) -> Tuple[date, int]:
        '''
        Return all dates we want to verify for testing.
        '''
        for day, _ in self.visited_uniques(include_today=True):
            yield day

        for day, _ in self.visited_repeats():
            yield day

    # -------------------------------------------------------------------------
    # UUIDs
    # -------------------------------------------------------------------------

    def uuid_random(self) -> uuid.UUID:
        '''
        Get a random UUID (uses uuid.uuid4()).
        '''
        return uuid.uuid4()

    def user_name(self, name: Union[str, date]) -> str:
        '''
        Ensures `name` is a string. If it is a date, converts to ISO-8601
        string.
        '''
        if isinstance(name, date):
            name = date.isoformat()
        return name

    def uuid_repeatable(self, *names: Union[str, date]) -> uuid.UUID:
        '''
        Get a _NON-RANDOM_ UUID!!!

        Used for testing repeat users where a predefined uuid is desirable.
        e.g. for rerunning tests without clearing the database and ensuring the
        predefined counts don't change.
        '''
        # Convert each name to string, join for a 'full name'.
        full_name = '.'.join([self.user_name(each) for each in names])

        # Convert to a UUID in a reproducable manner and return.
        return uuid.uuid5(self._UUID_NAMESPACE, full_name)

    # -------------------------------------------------------------------------
    # Dates
    # -------------------------------------------------------------------------

    def _range_day(self, day: date) -> Tuple[int, int]:
        '''
        Converts a day into a tuple range of unix timestamps for day start/day
        end seconds since unix epoch.

        Range returned is [day, next-day).
          - That is, both are midnight.
        '''
        start = datetime(day.year, day.month, day.day,
                         hour=0,
                         minute=0,
                         second=0,
                         tzinfo=timezone.utc)

        end = start + timedelta(days=1)

        return (int(start.timestamp()),
                int(end.timestamp()))

    def random_timestamp(self, day: date) -> int:
        '''
        Returns a random unix epoch timestamp that is some time during `day`.

        Timestamp is of seconds resolution.
        '''
        return random.randrange(*self._range_day(day))

    def expected(self, start: date, end: Optional[date] = None) -> int:
        '''
        Returns the number of users in date range: [`start`, `end`].

        - NOTE: Inclusive of `start` and `end` because we are comparing days
          and expecting all users who visited within:
            [midnight of start, midnight of day after end)
          Which, when using just dates, is equal to:
            [start, end]

        - NOTE: If `end` is None, returns the number of users in:
            [start, start]
        '''
        if not end:
            end = start

        total = 0
        for day, count in self.visited_uniques(include_today=True):
            # Inclusive!
            if start <= day <= end:
                total += count

        for day, users in self.visited_repeats():
            # Inclusive!
            if start <= day <= end:
                # Only count each repeated user once for this day.
                total += len(users)

        return total
