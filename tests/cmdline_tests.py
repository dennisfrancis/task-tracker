#!/usr/bin/env python

import unittest
import sys
from pathlib import Path

source_dir = Path(__file__).parent.parent.resolve() / "src"
sys.path.append(str(source_dir))

print(str(source_dir))

from tasktracker.actions import ActionAdd, ActionDelete, ActionList, ActionMark, ActionUpdate
from tasktracker.cmdline import get_action
from tasktracker.status import Status

program_name = "task-tracker.py"

class TestCmdlineParser(unittest.TestCase):

    def test_no_args(self):
        action = get_action([program_name,])
        self.assertIsNone(action, "must return None if no arguments were passed")

    def test_incorrect_action(self):
        action = get_action([program_name, "transform"])
        self.assertIsNone(action, "must return None if incorrect action was passed")
        action = get_action([program_name, "sort"])
        self.assertIsNone(action, "must return None if incorrect action was passed")


class TestAddParser(unittest.TestCase):

    def test_add_no_arg(self):
        action = get_action([program_name, "add"])
        self.assertIsNone(action, "must return None if no arguments were passed for add action")

    def test_add_two_args(self):
        action = get_action([program_name, "add", "arg1", "arg2"])
        self.assertIsNone(action, "must return None if more than one argument were passed for add action")

    def test_add_one_arg(self):
        action = get_action([program_name, "add", "Task1"])
        self.assertIsInstance(action, ActionAdd, "must return an instance of ActionAdd")
        self.assertEqual(action.task_description, "Task1", "incorrect task description parsed")


class TestUpdateParser(unittest.TestCase):

    def test_update_no_arg(self):
        action = get_action([program_name, "update"])
        self.assertIsNone(action, "must return None if no arguments were passed for update action")

    def test_update_one_arg(self):
        action = get_action([program_name, "update", "arg1", ])
        self.assertIsNone(action, "must return None if only one argument was passed for update action")

    def test_invalid_task_id(self):
        action = get_action([program_name, "update", "arg1", "TaskDesc"])
        self.assertIsNone(action, "must return None if invalid task_id was passed")

    def test_update_two_args(self):
        action = get_action([program_name, "update", "1", "TaskDesc"])
        self.assertIsInstance(action, ActionUpdate, "must return an instance of ActionUpdate")
        self.assertEqual(action.task_id, 1, "incorrect task_id parsed")
        self.assertEqual(action.task_description, "TaskDesc", "incorrect task_description parsed")


class TestDeleteParser(unittest.TestCase):

    def test_delete_no_arg(self):
        action = get_action([program_name, "delete"])
        self.assertIsNone(action, "must return None if no arguments were passed for delete action")

    def test_delete_two_args(self):
        action = get_action([program_name, "delete", "arg1", "arg2"])
        self.assertIsNone(action, "must return None if more than one argument were passed for delete action")

    def test_invalid_task_id(self):
        action = get_action([program_name, "delete", "id43"])
        self.assertIsNone(action, "must return None if invalid task_id was passed")

    def test_delete_one_arg(self):
        action = get_action([program_name, "delete", "45"])
        self.assertIsInstance(action, ActionDelete, "must return an instance of ActionDelete")
        self.assertEqual(action.task_id, 45, "incorrect task_id parsed")


class TestMarkParser(unittest.TestCase):

    def test_mark_no_arg(self):
        action = get_action([program_name, "mark"])
        self.assertIsNone(action, "must return None if no arguments were passed for mark action")

    def test_mark_one_arg(self):
        action = get_action([program_name, "mark", "23", ])
        self.assertIsNone(action, "must return None if only one argument was passed for mark action")

    def test_invalid_task_id(self):
        action = get_action([program_name, "mark", "id43", "in_progress"])
        self.assertIsNone(action, "must return None if invalid task_id was passed")

    def test_mark_incorrect_second_arg(self):
        action = get_action([program_name, "mark", "1", "SomeWrongStatus"])
        self.assertIsNone(action, "must return None if an incorrect status is passed as second argument")

    def test_mark_todo_second_arg(self):
        action = get_action([program_name, "mark", "1", "todo"])
        self.assertIsInstance(action, ActionMark, "must return instance of ActionMark")
        self.assertEqual(action.task_id, 1, "incorrect task_id parsed")
        self.assertEqual(action.new_status, Status.TODO, "incorrect status parsed")

    def test_mark_in_progress_second_arg(self):
        action = get_action([program_name, "mark", "1", "in_progress"])
        self.assertIsInstance(action, ActionMark, "must return instance of ActionMark")
        self.assertEqual(action.task_id, 1, "incorrect task_id parsed")
        self.assertEqual(action.new_status, Status.IN_PROGRESS, "incorrect status parsed")

    def test_mark_done_second_arg(self):
        action = get_action([program_name, "mark", "1", "done"])
        self.assertIsInstance(action, ActionMark, "must return instance of ActionMark")
        self.assertEqual(action.task_id, 1, "incorrect task_id parsed")
        self.assertEqual(action.new_status, Status.DONE, "incorrect status parsed")


class TestListParser(unittest.TestCase):

    def test_list_no_arg(self):
        action = get_action([program_name, "list"])
        self.assertIsInstance(action, ActionList, "must return an instance of ActionList")
        self.assertEqual(action.status, Status.UNKNOWN, "if there is no list argument, the status must be set to UNKNOWN")

    def test_list_two_args(self):
        action = get_action([program_name, "list", "arg1", "arg2"])
        self.assertIsNone(action, "must return None if more than one argument were passed for list action")

    def test_list_one_arg_todo(self):
        action = get_action([program_name, "list", "todo"])
        self.assertIsInstance(action, ActionList, "must return an instance of ActionList")
        self.assertEqual(action.status, Status.TODO, "incorrect status parsed")

    def test_list_one_arg_in_progress(self):
        action = get_action([program_name, "list", "in_progress"])
        self.assertIsInstance(action, ActionList, "must return an instance of ActionList")
        self.assertEqual(action.status, Status.IN_PROGRESS, "incorrect status parsed")

    def test_list_one_arg_done(self):
        action = get_action([program_name, "list", "done"])
        self.assertIsInstance(action, ActionList, "must return an instance of ActionList")
        self.assertEqual(action.status, Status.DONE, "incorrect status parsed")


if __name__ == '__main__':
    unittest.main()

