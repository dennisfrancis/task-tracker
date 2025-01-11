#!/usr/bin/env python

"""Unit tests for TaskStore class"""

import unittest
import sys
from pathlib import Path
from typing import List, Optional, Dict
from time import sleep

current_dir = Path(__file__).parent
source_dir = current_dir.parent.resolve() / "src"
test_write_dir = current_dir / "write"
sys.path.append(str(source_dir))

from tasktracker.actions import ActionAdd, ActionDelete, ActionList, ActionMark, ActionUpdate
from tasktracker.tasks import TaskStore

class TestTaskStore(unittest.TestCase):

    def setUp(self):
        self.tmpdir = test_write_dir
        if not self.tmpdir.is_dir():
            self.tmpdir.mkdir()
        self.data_file= self.tmpdir / "tasks.json"
        self.data_fname = str(self.data_file)
        if self.data_file.is_file():
            self.data_file.unlink()

    def tearDown(self):
        if self.tmpdir.is_dir():
            self.data_file = Path(self.data_fname)
            if self.data_file.is_file():
                self.data_file.unlink()
            self.tmpdir.rmdir()

    def _load_store(self):
        return TaskStore(self.data_fname, test_mode = True)

    def _add_tasks(self, actions: List[ActionAdd], store: Optional[TaskStore] = None) -> TaskStore:
        if store is None:
            store = self._load_store()
        for action in actions:
            store.add(action)
        return store

    def _delete_tasks(self, actions: List[ActionDelete], store: Optional[TaskStore] = None) -> TaskStore:
        if store is None:
            store = self._load_store()
        for action in actions:
            store.delete(action)
        return store

    def _get_task_from_desc(self, task_desc: str, tasks: List[Dict[str, str]]) -> Dict[str, str]:
        found = False
        for task in tasks:
            if task["Description"] == task_desc:
                found = True
                return task.copy()
        self.assertTrue(found, "Cannot find a task with description='{}'".format(task_desc))
        return {}

    def assertTasksEqual(self, task_actual: Dict[str, str], task_expected: Dict[str, str], msg: str = ""):
        keyset = set(task_actual.keys()) & set(task_expected.keys())
        for key in keyset:
            self.assertEqual(task_actual[key], task_expected[key],
                             msg + "\nTask with Description='{}' has unexpected value for key={}". \
                                     format(task_actual["Description"], key))


    def assertHasTask(self, task_dict: Dict[str, str], tasks: List[Dict[str, str]]):
        found = False
        for task in tasks:
            if task["ID"] == task_dict["ID"]:
                self.assertTasksEqual(task, task_dict)
                found = True
                break
        self.assertTrue(found, "Task with ID={} not found".format(task_dict["ID"]))

    def test_setup_is_correct(self):
        self.assertTrue(self.tmpdir.is_dir())
        self.assertTrue(not Path(self.data_fname).is_file())

    def test_store_check_empty(self):
        store = self._load_store()
        tasks = store.get_task_list()
        self.assertEqual(len(tasks), 0, "Store should be empty at the beginning")

    def test_store_add(self):
        task1_desc = "Task 1"
        task2_desc = "Task 2"
        store = self._add_tasks([ActionAdd([task1_desc,])])
        tasks = store.get_task_list()

        self.assertEqual(len(tasks), 1, "There must be exactly one task after first addition")
        task1_expected = self._get_task_from_desc(task1_desc, tasks)
        self.assertEqual(task1_expected["Updated@"], task1_expected["Created@"],
                         "Updated@ must match Created@ for a brand new task")

        store = self._load_store()
        tasks = store.get_task_list()
        self.assertEqual(len(tasks), 1, "There must be exactly one task after first addition")
        self.assertHasTask(task1_expected, tasks)

        self._add_tasks([ActionAdd([task2_desc,])], store)
        task2_expected = self._get_task_from_desc(task2_desc, store.get_task_list())
        self.assertEqual(task2_expected["Updated@"], task2_expected["Created@"],
                         "Updated@ must match Created@ for a brand new task")

        store = self._load_store()
        tasks = store.get_task_list()
        self.assertEqual(len(tasks), 2)
        self.assertHasTask(task1_expected, tasks)
        self.assertHasTask(task2_expected, tasks)

    def test_store_delete(self):
        task1_desc = "Task 1"
        task2_desc = "Task 2"
        store = self._load_store()
        self._delete_tasks([ActionDelete(["100"]),], store)
        self._add_tasks([
            ActionAdd([task1_desc,]),
            ActionAdd([task2_desc,]),], store)

        store = self._load_store()
        tasks = store.get_task_list()
        task1= self._get_task_from_desc(task1_desc, tasks)
        task2 = self._get_task_from_desc(task2_desc, tasks)
        self.assertEqual(len(tasks), 2)
        store.delete(ActionDelete([task1["ID"],]))

        store = self._load_store()
        tasks = store.get_task_list()
        self.assertEqual(len(tasks), 1)
        self.assertTasksEqual(tasks[0], task2)
        store.delete(ActionDelete([task1["ID"],]))
        del store
        store = self._load_store()
        tasks = store.get_task_list()
        self.assertEqual(len(tasks), 1)
        self.assertTasksEqual(tasks[0], task2)
        store.delete(ActionDelete([task2["ID"],]))

        store = self._load_store()
        tasks = store.get_task_list()
        self.assertEqual(len(tasks), 0)

    def test_store_update(self):
        task1_desc = "Task 1"
        task2_desc = "Task 2"
        task3_desc = "Task 3"
        store = self._load_store()
        self._add_tasks([
            ActionAdd([task1_desc,]),
            ActionAdd([task2_desc,]),
            ActionAdd([task3_desc,]),], store)
        tasks = store.get_task_list()
        task1, task2, task3 = [ self._get_task_from_desc(desc, tasks) \
                for desc in (task1_desc, task2_desc, task3_desc) ]

        store = self._load_store()
        sleep(1)
        store.update(ActionUpdate(["200", "XYZ"]))
        task2["Description"] = "Task 2 updated msg"
        store.update(ActionUpdate([task2["ID"], task2["Description"]]))
        tasks = store.get_task_list()
        task2["Updated@"] = self._get_task_from_desc(task2["Description"], tasks)["Updated@"]

        store = self._load_store()
        tasks = store.get_task_list()
        self.assertHasTask(task1, tasks)
        self.assertHasTask(task2, tasks)
        self.assertHasTask(task3, tasks)

        task1["Description"] = task1["Description"] + " addendum"
        sleep(1)
        store.update(ActionUpdate([task1["ID"], task1["Description"]]))
        tasks = store.get_task_list()
        task1["Updated@"] = self._get_task_from_desc(task1["Description"], tasks)["Updated@"]

        store = self._load_store()
        tasks = store.get_task_list()
        self.assertHasTask(task1, tasks)
        self.assertHasTask(task2, tasks)
        self.assertHasTask(task3, tasks)


if __name__ == '__main__':
    unittest.main()
