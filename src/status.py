#!/usr/bin/env python

from enum import Enum

class Status(Enum):
    TODO = 1
    IN_PROGRESS = 2
    DONE = 3
    UNKNOWN = 101

def _get_status_names():
    return [status.name.lower() for status in Status if status != Status.UNKNOWN]

