# coding: utf-8

'''
Helpers for dealing with timestamps.
'''

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

from typing import Optional, Union, Type, NewType, Dict, Tuple, TextIO

from datetime import date, datetime, time, timedelta


# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# Code
# -----------------------------------------------------------------------------


class UnixEpoch:
    '''
    Functions for 'seconds since the Unix Epoch'.
    '''

    @classmethod
    def parse(klass: Type['UnixEpoch'],
              input: Union[str, int, float, None]) -> float:
        '''
        Parse `input` into a unix timestamp.

        Raises ValueError if input is not None and cannot be parsed to float.
        '''
        unixtime = None
        if input:
            # Can raise ValueError
            unixtime = float(input)

        # Use UTC NOW as time if input was 'None'.
        if not unixtime:
            unixtime = klass.now()

        return unixtime

    @classmethod
    def seconds(klass: Type['UnixEpoch'],
                timestamp: Union[int, float]) -> int:
        '''
        Convert a timestamp into seconds resolution.
        '''
        return int(timestamp)

    @classmethod
    def now(klass: Type['UnixEpoch']) -> float:
        '''
        Returns datetime.utcnow() as a unix timestamp.
        '''
        return datetime.utcnow().timestamp()

    @classmethod
    def range_day(klass: Type['UnixEpoch'],
                  day: date) -> Tuple[int, int]:
        '''
        Converts a day into a tuple range of unix timestamps for day start/day
        end seconds since unix epoch.

        Range returned is [day, next-day).
          - That is, both are midnight.
        '''
        start = datetime(day.year, day.month, day.day,
                         hour=0,
                         minute=0,
                         second=0)

        end = start + timedelta(days=1)

        return (klass.seconds(start.timestamp()),
                klass.seconds(end.timestamp()))

    @classmethod
    def range_month(klass: Type['UnixEpoch'],
                    day: date) -> Tuple[int, int]:
        '''
        Converts a day into a tuple range of unix timestamps for month
        start/month end seconds since unix epoch.

        If `day` input is YYYY-MM-DD, then the range returned is:
        [ YYYY-MM-01, (YYYY-MM-DD)+(1 day) ).
        '''
        start = datetime(day.year, day.month, 1,
                         hour=0,
                         minute=0,
                         second=0)

        end = (datetime(day.year, day.month, day.day,
                        hour=0,
                        minute=0,
                        second=0)
               + timedelta(days=1))

        return (klass.seconds(start.timestamp()),
                klass.seconds(end.timestamp()))


class Iso8601:
    '''
    Functions for ISO-8601 datetime format.

    The best datetime format.
    '''

    @classmethod
    def parse(klass: Type['Iso8601'],
              input: str) -> date:
        '''
        Parse `input` into a unix timestamp.

        Raises ValueError if input is not None and cannot be parsed to float.
        '''
        return datetime.fromisoformat(input).date()
