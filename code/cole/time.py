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
