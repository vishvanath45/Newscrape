"""
A set of functions commonly used in the Newscrape project.
"""

from datetime import datetime, timezone, timedelta
from bs4 import NavigableString, Comment


def str_is_set(string):
    """
    Return False if string is empty True otherwise.
    """
    return string


def is_string(obj):
    """
    Returns True if obj is string False if not.
    """
    return not isinstance(obj, Comment) and isinstance(obj, NavigableString)


def to_utc(timestamp):
    return timestamp.astimezone(tz=timezone.utc)


def set_ist_zone(timestamp):
    timestamp.replace(
        tzinfo=timezone(timedelta(hours=5, minutes=30))
    )


def ist_to_utc(timestamp):
    set_ist_zone(timestamp)
    return to_utc(timestamp)


def remove_duplicate_entries(objects, key):
    """
    Return a new list of objects after removing all duplicate objects based on
    key.
    """
    unique_set = set()
    def is_unique(obj):
        "Return False x[key] is present in set, True otherwise."
        if obj[key] not in unique_set:
            unique_set.add(obj[key])
            return True
        return False
    return list(filter(is_unique, objects))
