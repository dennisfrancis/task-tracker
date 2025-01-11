#!/usr/bin/env python

"""Unit tests for TaskStore class"""

import unittest
import sys
from pathlib import Path

current_dir = Path(__file__).parent
source_dir = current_dir.parent.resolve() / "src"
test_write_dir = current_dir / "write"
sys.path.append(str(source_dir))

from tasktracker.actions import ActionAdd, ActionDelete, ActionList, ActionMark, ActionUpdate
from tasktracker.status import Status
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

    def test_setup_is_correct(self):
        self.assertTrue(self.tmpdir.is_dir())
        self.assertTrue(not Path(self.data_fname).is_file())

    def test_store_check_empty(self):
        store = TaskStore(self.data_fname, test_mode = True)
        tasks = store.get_task_list()
        self.assertEqual(len(tasks), 0, "Store should be empty at the beginning")

    def test_store_add(self):
        task1_desc = "Task 1"
        store = TaskStore(self.data_fname, test_mode = True)
        store.add(ActionAdd([task1_desc,]))
        tasks = store.get_task_list()

        self.assertEqual(len(tasks), 1, "There must be exactly one task after addition")
        self.assertEqual(tasks[0]["Description"], task1_desc, "Task description not preserved")
        self.assertEqual(tasks[0]["Created@"], tasks[0]["Updated@"],
                         "Created time must be the same as updated time")
        tstamp = tasks[0]["Created@"]
        del store
        store = TaskStore(self.data_fname, test_mode = True)
        tasks = store.get_task_list()

        self.assertEqual(len(tasks), 1, "There must be exactly one task after addition")
        self.assertEqual(tasks[0]["Description"], task1_desc, "Task description not preserved")
        self.assertEqual(tasks[0]["Created@"], tasks[0]["Updated@"],
                         "Created time must be the same as updated time")
        self.assertEqual(tasks[0]["Created@"], tstamp, "Timestamp does not persist correctly")

    def test_store_delete(self):
        task1_desc = "Task 1"
        task2_desc = "Task 2"
        store = TaskStore(self.data_fname, test_mode = True)
        store.delete(ActionDelete(["100"]))
        store.add(ActionAdd([task1_desc,]))
        store.add(ActionAdd([task2_desc,]))
        del store
        store = TaskStore(self.data_fname, test_mode = True)
        tasks = store.get_task_list()
        self.assertEqual(len(tasks), 2)
        store.delete(ActionDelete(["1"]))
        del store
        store = TaskStore(self.data_fname, test_mode = True)
        tasks = store.get_task_list()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["ID"], "2")
        self.assertEqual(tasks[0]["Description"], task2_desc)
        store.delete(ActionDelete(["1"]))
        del store
        store = TaskStore(self.data_fname, test_mode = True)
        tasks = store.get_task_list()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["ID"], "2")
        self.assertEqual(tasks[0]["Description"], task2_desc)
        store.delete(ActionDelete(["2"]))
        del store
        store = TaskStore(self.data_fname, test_mode = True)
        tasks = store.get_task_list()
        self.assertEqual(len(tasks), 0)


if __name__ == '__main__':
    unittest.main()
