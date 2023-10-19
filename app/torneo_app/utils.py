import datetime
from enum import Enum

import pytz


def now():
    return datetime.datetime.now(pytz.utc)


def is_in_past(date):
    return date < now()


def is_in_future(date):
    return date > now()


def str_empty(s: str) -> bool:
    return s and s.strip() != ""


class UserStatus(Enum):
    NORMAL = 0
    ORGANIZER = 1
    APPLIED = 2
