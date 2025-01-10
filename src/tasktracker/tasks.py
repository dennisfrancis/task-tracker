#!/usr/bin/env python

"""Implements task management functionality"""

import sys
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import override, Any, cast, Dict, List, Generator

from tasktracker.actions import *
from tasktracker.status import Status, status_map
from tasktracker.tables import show_table

class Task:
    """
    Task represents a single task with id(tid), a short
    description(description), its status and two datetime fields to represent
    when it was created and when it was updated last both in UTC timezone.
    """

    tid = -1
    description = ""
    status = Status.UNKNOWN
    created_at = datetime(1970, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    updated_at = datetime(1970, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

    def __lt__(self, other):
        """
        When sorting a list of tasks, order by status. For tasks of same
        status, order by last updated time in descending order.
        """
        if self.status.value < other.status.value:
            return True
        if self.status.value > other.status.value:
            return False
        if self.updated_at < other.updated_at:
            return False
        return True

    def to_dict(self) -> Dict[str, str]:
        fmt_str = "%d %b %Y %H:%M:%S"
        return {
                "ID" : str(self.tid),
                "Description" : self.description,
                "Status" : self.status.name.lower(),
                "Updated@" : self.updated_at.astimezone().strftime(fmt_str),
                "Created@" : self.created_at.astimezone().strftime(fmt_str) }

    @staticmethod
    def column_names() -> List[str]:
        return [ "ID", "Description", "Status", "Updated@", "Created@" ]


class TaskEncoder(json.JSONEncoder):
    """
    A custom JSON encoder for Task instances. The status is represented by
    lower case strings. The created_at and updated_at datetimes are represented
    as timestamps. Task is represented as a dictionary with a special key value
    pair of <"__class__" : "Task"> as a cue to the decoder (TaskDecoder).
    """
    @override
    def default(self, o):
        if not isinstance(o, Task):
            return super().default(o)
        return {
                "__class__": "Task",
                "tid" : o.tid,
                "description" : o.description,
                "status" : o.status.name.lower(),
                "created_at" : str(o.created_at.timestamp()),
                "updated_at": str(o.updated_at.timestamp()) }

class TaskDecoder(json.JSONDecoder):
    """
    A custom JSON decoder for importing Task instances from JSON. This reverses
    the convertions done in TaskEncoder to read dictionaries representing a
    task to a Task instance.
    """
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=TaskDecoder.from_dict)

    @staticmethod
    def from_dict(d):
        if d.get("__class__") != "Task":
            return d
        task = Task()
        task.tid = int(d["tid"])
        task.description = d["description"]
        task.status = status_map[d["status"]]
        task.created_at = datetime.fromtimestamp(float(d["created_at"]), tz=timezone.utc)
        task.updated_at = datetime.fromtimestamp(float(d["updated_at"]), tz=timezone.utc)
        return task

class TaskStore:
    """
    TaskStore is an abstraction that handles the underlying JSON file
    read/write operations while providing the api for adding a new task,
    updating a task, deleting a task, marking a task and listing all existing
    tasks or those with of a specific status.
    """

    error = False #  To indicate one or more errors occured.

    # In-memory representation of list of Tasks.
    # "next_tid" holds the value of "task id" for the next Task to be added.
    _store: dict[int | str, Any] = { "next_tid" : 1 }

    def __init__(self, store_fname: str, test_mode = False) -> None:
        """
        Builds a TaskStore instance from the given file path of the underlying
        JSON data file. If the file does not exist, it is created.
        """

        self.file = store_fname
        self.test_mode = test_mode
        if not Path(self.file).is_file():
            self._write()

        try:
            with open(self.file, "r") as fp:
                self._load(fp)
        except Exception:
            print("[ERROR] cannot load data file {} due to possible corruption.".format(self.file))
            self.error = True

    def _load(self, fp):
        """
        Imports tasks from the JSON data file to be held in memory making use
        of the custom JSON decoder(TaskDecoder).
        """

        self._store = json.load(fp, cls=TaskDecoder)

    def _write(self):
        """
        Exports the tasks data from the in memory representation in self._store
        to the JSON file making use of the custom JSON encoder(TaskEncoder).
        """

        try:
            with open(self.file, "w") as fp:
                json.dump(self._store, fp, cls=TaskEncoder)
        except Exception:
            print("[ERROR] cannot write to {}.".format(self.file))
            self.error = True

    def _next_tid(self) -> int:
        """
        Helper method to provide a "task id" for the next task. This also
        increments the internal counter in the in memory store.
        """

        next_tid = self._store["next_tid"]
        self._store["next_tid"] += 1
        return next_tid

    def _get_task(self, tid: int) -> Task | None:
        """
        Helper method to get a Task instance corresponding to a task-id from
        the in-memory store.
        """

        stid = str(tid)
        if stid not in self._store:
            return None
        return self._store[stid]

    def add(self, action: ActionAdd):
        """
        Adds a new task with description specified by action(ActionAdd
        instance) to the in-memory data store and finally writes everything
        to JSON file.
        """

        next_tid = self._next_tid()
        task = Task()
        task.tid = next_tid
        task.description = action.task_description
        task.status = Status.TODO
        now = datetime.now(tz=timezone.utc)
        task.created_at = now
        task.updated_at = now
        self._store[task.tid] = task
        self._write()
        if not self.error and not self.test_mode:
            print("Added new task with id = {}".format(next_tid))
            show_table([task.to_dict(),], Task.column_names(), {"Description": 60})

    def update(self, action: ActionUpdate):
        """
        Updates the description of a task in the in-memory store for a given
        task-id specified by the "action" parameter. The in-memory store is
        serialized to JSON in the end.
        """

        task = self._get_task(action.task_id)
        if task is None:
            if not self.test_mode:
                print("[ERROR] There is no task with task_id = {}".format(action.task_id))
            return
        task.description = action.task_description
        now = datetime.now(tz=timezone.utc)
        task.updated_at = now
        self._write()
        if not self.error and not self.test_mode:
            print("Updated task with id = {}".format(action.task_id))
            show_table([task.to_dict(),], Task.column_names(), {"Description": 60})

    def delete(self, action: ActionDelete):
        """
        Deletes a task specified by the action parameter from the in-memory
        store and finally the JSON file is re-written.
        """

        stid = str(action.task_id)
        if stid not in self._store:
            if not self.test_mode:
                print("[ERROR] There is no task with task_id = {}".format(action.task_id))
            return
        task = self._store[stid]
        del self._store[stid]
        self._write()
        if not self.error and not self.test_mode:
            print("Deleted task with id = {}".format(action.task_id))
            show_table([task.to_dict(),], Task.column_names(), {"Description": 60})

    def get_task_list(self, status: Status = Status.UNKNOWN) -> List[Dict[str, str]]:
        """
        Method to get a sorted list of all tasks or those with a given status.
        """
        tasks: Generator[Task, None, None] = (task for _, task in self._store.items() if hasattr(task, "tid"))
        if status != Status.UNKNOWN:
            tasks = (task for task in tasks if task.status == status)
        tasks_sorted = sorted(tasks)
        return [ task.to_dict() for task in tasks_sorted ]

    def list(self, action: ActionList):
        """
        Lists the all existing tasks or those with a status specified by the
        action parameter.
        """

        data = self.get_task_list(action.status)
        if len(data):
            if action.status == Status.UNKNOWN:
                print("\nList of all tasks:")
            else:
                print("\nList of {} tasks:".format(action.status.name.lower()))

            show_table(data, Task.column_names(), {"Description": 60})
        else:
            print("There are no {}tasks.".format("" if action.status == Status.UNKNOWN else action.status.name.lower() + " "))

    def mark(self, action: ActionMark):
        """
        Changes the status of a task as specified by the action parameter and the JSON file is updated.
        """

        task = self._get_task(action.task_id)
        if task is None:
            if not self.test_mode:
                print("[ERROR] There is no task with task_id = {}".format(action.task_id))
            return
        task.status = action.new_status
        now = datetime.now(tz=timezone.utc)
        task.updated_at = now
        self._write()
        if not self.error and not self.test_mode:
            print("Marked task with id = {} as {}".format(action.task_id, action.new_status.name.lower()))
            show_table([task.to_dict(),], Task.column_names(), {"Description": 60})


class TasksManager:
    """
    Executes the sub-commands from CLI by forwarding the actions to TaskStore
    API.
    """

    error = False # To store the error status of one of the store or file operations.
    def __init__(self, data_fname : str | None = None) -> None:
        """
        Creates an instance of TaskStore from the default or specified JSON
        file.
        """

        if data_fname is None:
            try:
                self.file = self._default_data_fname()
            except:
                print("[ERROR] Cannot create default data directory!")
                self.error = True
                return
        else:
            self.file = data_fname
        if self.error:
            return
        self.store = TaskStore(str(self.file))
        if self.store.error:
            self.error = True

    def _default_data_fname(self) -> Path:
        """
        Helper method that returns the default JSON file location.
        """

        folder = self._data_dir()
        if not folder.is_dir():
            folder.mkdir(parents=True)
        return folder / "tasks.json"

    def _data_dir(self) -> Path:
        """
        Returns a parent directory path
        where persistent application data can be stored.

        # linux: ~/.local/share
        # macOS: ~/Library/Application Support
        # windows: C:/Users/<USER>/AppData/Roaming

        Adapted from: https://stackoverflow.com/a/61901696
        """

        home = Path.home()
        dir_name = "task-tracker"
        if sys.platform == "win32":
            return home / "AppData/Roaming" / dir_name
        elif sys.platform == "linux":
            return home / ".local/share" / dir_name
        elif sys.platform == "darwin":
            return home / "Library/Application Support" / dir_name

    def execute(self, action: ActionBase):
        """
        Forwards the action parameter to the TaskStore instance's
        corresponding API method.
        """

        if self.error:
            print("[ERROR] Cannot continue due to previous error(s)")
            return
        if action.atype == ActionType.ADD:
            self.store.add(cast(ActionAdd, action))
        elif action.atype == ActionType.UPDATE:
            self.store.update(cast(ActionUpdate, action))
        elif action.atype == ActionType.DELETE:
            self.store.delete(cast(ActionDelete, action))
        elif action.atype == ActionType.LIST:
            self.store.list(cast(ActionList, action))
        elif action.atype == ActionType.MARK:
            self.store.mark(cast(ActionMark, action))

