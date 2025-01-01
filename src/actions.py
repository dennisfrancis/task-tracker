#!/usr/bin/env python

from enum import Enum
from status import Status
from typing import override


class ActionType(Enum):
    ADD = 1
    UPDATE = 2
    DELETE = 3
    LIST = 4
    MARK = 5
    UNKNOWN = 100

class ActionBase:
    atype: ActionType = ActionType.UNKNOWN
    def help(self):
        pass

class ActionAdd(ActionBase):
    task_description: str = ''

    def __init__(self, args: list[str]) -> None:
        super().__init__()

    @override
    def help(self):
        pass

class ActionUpdate(ActionBase):
    task_description: str = ''
    task_id: int = -1

    def __init__(self, args: list[str]) -> None:
        super().__init__()

    @override
    def help(self):
        pass

class ActionDelete(ActionBase):
    task_id: int = -1

    def __init__(self, args: list[str]) -> None:
        super().__init__()

    @override
    def help(self):
        pass

class ActionList(ActionBase):
    status: Status = Status.UNKNOWN

    def __init__(self, args: list[str]) -> None:
        super().__init__()

    @override
    def help(self):
        pass

class ActionMark(ActionBase):
    task_id: int = -1
    new_status: Status = Status.UNKNOWN

    def __init__(self, args: list[str]) -> None:
        super().__init__()

    @override
    def help(self):
        pass

