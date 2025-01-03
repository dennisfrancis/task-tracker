#!/usr/bin/env python

from enum import Enum

class Status(Enum):
    TODO = 1
    IN_PROGRESS = 2
    DONE = 3
    UNKNOWN = 101

_status_map = {
        status.name.lower(): status for status in Status if status != Status.UNKNOWN }

def get_status_names():
    return [status.name.lower() for status in Status if status != Status.UNKNOWN]

def get_status_from_str(status_str: str) -> Status | None:
    try:
        status = _status_map[status_str]
    except KeyError:
        return None
    return status

