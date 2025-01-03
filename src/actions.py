#!/usr/bin/env python

from enum import Enum
from status import Status, get_status_from_str, get_status_names
from typing import override

program_name = 'task-tracker.py'

class ActionType(Enum):
    ADD = 1
    UPDATE = 2
    DELETE = 3
    LIST = 4
    MARK = 5
    UNKNOWN = 100

class ActionBase:
    atype: ActionType = ActionType.UNKNOWN
    def __init__(self, atype: ActionType) -> None:
        self.atype = atype

    def help(self):
        pass

class ActionAdd(ActionBase):
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
        print("Where status is one of {}".format(get_status_names()))


class ActionMark(ActionBase):
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
        print("Where status is one of {}".format(get_status_names()))

