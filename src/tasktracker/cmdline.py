#!/usr/bin/env python

"""Utilities to parse command-line arguments and show usage"""

from tasktracker.formatting import fmt_list_of_strings
from tasktracker.actions import *

_action_map = {
              "add" : ActionAdd,
              "update" : ActionUpdate,
              "delete" : ActionDelete,
              "list" : ActionList,
              "mark" : ActionMark }

def get_action(args: list[str], show_help=False) -> ActionBase | None:
    """\
    Accepts the command-line arguments, parses them and returns the appropriate
    Action* instance representing the user request.

    Keyword arguments:
    args: list of command-line arguments. Typically sys.args is passed.
    show_help: If set to True shows the usage help if the arguments corresponds
               to an invalid sub-command.
    """
    if len(args) == 1:
        return None
    try:
        action_class = _action_map[args[1]]
    except KeyError:
        return None
    action = action_class(args[2:])
    if show_help and not action.valid:
        action.help()
    return None if not action.valid else action

def _get_action_names():
    return [action.name.lower() for action in ActionType if action != ActionType.UNKNOWN]

def show_usage():
    """Displays general command-line usage help"""
    print("\nGeneral Usage: task-tracker <action> <action-arguments...>")
    print("\nWhere action can be one of {}".format(fmt_list_of_strings(_get_action_names())))
    return

