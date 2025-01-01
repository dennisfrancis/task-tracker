#!/usr/bin/env python

"""Utilities to parse command-line arguments and show usage"""

from actions import *

class Parameters:
    action = ActionBase()
    args: list[str] = []

def get_params(args: list[str]):
    return None

def _get_action_names():
    return [action.name.lower() for action in ActionType if action != ActionType.UNKNOWN]

def show_usage():
    print("Usage: task-tracker <action> <action-arguments...>")
    print("\nWhere action can be one of {}".format(_get_action_names()))
    return

