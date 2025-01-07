#!/usr/bin/env python

"""\
This module contains the enum type representing the status of a task and
related utility functions.
"""
from enum import Enum

class Status(Enum):
    """Status of each task"""
    TODO = 1
    IN_PROGRESS = 2
    DONE = 3
    UNKNOWN = 101

status_map = {
        status.name.lower(): status for status in Status if status != Status.UNKNOWN }

def get_status_names():
    """Returns the display names of each status state"""
    return [status.name.lower() for status in Status if status != Status.UNKNOWN]

def get_status_from_str(status_str: str) -> Status | None:
    """Returns the status enum item corresponding to the given display string
    if valid else None is returned"""
    try:
        status = status_map[status_str]
    except KeyError:
        return None
    return status

