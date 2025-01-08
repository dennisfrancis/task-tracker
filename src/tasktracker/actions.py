#!/usr/bin/env python

"""\
Collection of classes for representing the different actions to perform that
correspond to each user sub-command
"""

from enum import Enum
from typing import override
from tasktracker.status import Status, get_status_from_str, get_status_names
from tasktracker.formatting import fmt_list_of_strings

program_name = 'task-tracker'

class ActionType(Enum):
    """Represents the type of action"""
    ADD = 1
    UPDATE = 2
    DELETE = 3
    LIST = 4
    MARK = 5
    UNKNOWN = 100

class ActionBase:
    """Base class of all action classes"""
    atype: ActionType = ActionType.UNKNOWN
    def __init__(self, atype: ActionType) -> None:
        self.atype = atype

    def help(self):
        pass

class ActionAdd(ActionBase):
    """Action that corresponds to the creation of a new task"""
    task_description: str = ''
    valid = False

    def __init__(self, args: list[str]):
        super().__init__(ActionType.ADD)
        if len(args) != 1:
            return
        self.valid = True
        self.task_description = args[0]

    @override
    def help(self):
        print("Subcommand usage:\n{} add <task_description>".format(program_name))

class ActionUpdate(ActionBase):
    """Action that corresponds to the updation of an existing task"""
    task_description: str = ''
    task_id: int = -1
    valid = False

    def __init__(self, args: list[str]) -> None:
        super().__init__(ActionType.UPDATE)
        if len(args) != 2:
            return
        try:
            self.task_id = int(args[0])
        except ValueError:
            return
        self.task_description = args[1]
        self.valid = True

    @override
    def help(self):
        print("Subcommand usage:\n{} update <task_id:integer> <task_description>".format(program_name))


class ActionDelete(ActionBase):
    """Action that corresponds to the deletion of an existing task"""
    task_id: int = -1
    valid = False

    def __init__(self, args: list[str]) -> None:
        super().__init__(ActionType.DELETE)
        if len(args) != 1:
            return
        try:
            self.task_id = int(args[0])
        except ValueError:
            return
        self.valid = True

    @override
    def help(self):
        pass


class ActionList(ActionBase):
    """Action that corresponds to the listing of existing tasks"""
    status: Status = Status.UNKNOWN
    valid = False

    def __init__(self, args: list[str]) -> None:
        super().__init__(ActionType.LIST)
        if len(args) == 0:
            self.valid = True
            return
        if len(args) != 1:
            return

        _status = get_status_from_str(args[0])
        if _status is None:
            return
        self.status = _status
        self.valid = True

    @override
    def help(self):
        print("Subcommand usage:\n{} list [status]".format(program_name))
        print("Where status is one of {}".format(fmt_list_of_strings(get_status_names())))


class ActionMark(ActionBase):
    """"ActionMark represent the user request to update the status of an existing task"""
    task_id: int = -1
    new_status: Status = Status.UNKNOWN
    valid = False

    def __init__(self, args: list[str]) -> None:
        super().__init__(ActionType.MARK)
        if len(args) != 2:
            return

        try:
            self.task_id = int(args[0])
        except ValueError:
            return
        _status = get_status_from_str(args[1])
        if _status is None:
            return
        self.new_status = _status
        self.valid = True

    @override
    def help(self):
        print("Subcommand usage:\n{} mark <task_id:integer> <status>".format(program_name))
        print("Where status is one of {}".format(fmt_list_of_strings(get_status_names())))

