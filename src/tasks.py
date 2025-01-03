#!/usr/bin/env python

"""Implements task management functionality"""

import sys
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import override, Any, cast
from actions import *
from status import Status, status_map

class Task:
    tid = -1
    description = ""
    status = Status.UNKNOWN
    created_at = datetime(1970, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    updated_at = datetime(1970, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

    def __lt__(self, other):
        if self.status.value < other.status.value:
            return True
        if self.status.value > other.status.value:
            return False
        if self.updated_at < other.updated_at:
            return False
        return True

class TaskEncoder(json.JSONEncoder):
    @override
    def default(self, o):
        if not isinstance(o, Task):
            return super().default(o)
        return {"__class__": "Task",
                "tid" : o.tid,
                "description" : o.description,
                "status" : o.status.name.lower(),
                "created_at" : str(o.created_at.timestamp()),
                "updated_at": str(o.updated_at.timestamp()) }

class TaskDecoder(json.JSONDecoder):
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
    error = False
    _store: dict[int | str, Any] = { "next_tid" : 1 }
    def __init__(self, store_fname: str) -> None:
        self.file = store_fname
        if not Path(self.file).is_file():
            self._write()
        try:
            with open(self.file, "r") as fp:
                self._load(fp)
        except Exception as e:
            print("[ERROR] cannot load data file {} due to possible corruption.".format(self.file))
            self.error = True

    def _load(self, fp):
        self._store = json.load(fp, cls=TaskDecoder)

    def _write(self):
        try:
            with open(self.file, "w") as fp:
                json.dump(self._store, fp, cls=TaskEncoder)
        except Exception as e:
            print("[ERROR] cannot write to {}.".format(self.file))
            self.error = True

    def _next_tid(self) -> int:
        next_tid = self._store["next_tid"]
        self._store["next_tid"] += 1
        return next_tid

    def _get_task(self, tid: int) -> Task | None:
        stid = str(tid)
        if stid not in self._store:
            return None
        return self._store[stid]

    def add(self, action: ActionAdd):
        assert action.valid
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
        if not self.error:
            print("Added new task with id = {}".format(next_tid))

    def update(self, action: ActionUpdate):
        task = self._get_task(action.task_id)
        if task is None:
            print("[ERROR] There is no task with task_id = {}".format(action.task_id))
            return
        task.description = action.task_description
        now = datetime.now(tz=timezone.utc)
        task.updated_at = now
        self._write()
        if not self.error:
            print("Updated task with id = {}".format(action.task_id))

    def delete(self, action: ActionDelete):
        stid = str(action.task_id)
        if stid not in self._store:
            print("[ERROR] There is no task with task_id = {}".format(action.task_id))
            return
        del self._store[stid]
        self._write()
        if not self.error:
            print("Deleted task with id = {}".format(action.task_id))

    def list(self, action: ActionList):
        tasks = (task for key, task in self._store.items() if hasattr(task, "tid"))
        if action.status != Status.UNKNOWN:
            tasks = (task for task in tasks if task.status == action.status)
        tasks = sorted(tasks)
        desc_max = 80
        print("{} tasks:".format("All" if action.status == Status.UNKNOWN else action.status.name.capitalize()))
        print("{:<3} | {:<80} | {:<12} | {:<20}".format("Id", "Description", "Status", "Updated at"))
        print("{:<3}-+-{:<80}-+-{:<12}-+-{:<20}".format("-"*3, "-"*desc_max, "-"*12, "-"*20))
        for task in tasks:
            desc = task.description
            if len(desc) > desc_max:
                desc = desc[:desc_max-3] + "..."
            print("{:<3} | {:<80} | {:<12} | {:<20}".
                  format(task.tid, desc, task.status.name.lower(), task.updated_at.astimezone().strftime("%d %b %Y %H:%M:%S")))

    def mark(self, action: ActionMark):
        task = self._get_task(action.task_id)
        if task is None:
            print("[ERROR] There is no task with task_id = {}".format(action.task_id))
            return
        task.status = action.new_status
        now = datetime.now(tz=timezone.utc)
        task.updated_at = now
        self._write()
        if not self.error:
            print("Marked task with id = {} as {}".format(action.task_id, action.new_status.name.lower()))

class TasksManager:
    error = False
    def __init__(self, data_fname : str | None = None) -> None:
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

        https://stackoverflow.com/a/61901696
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

