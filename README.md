# task-tracker
Task-tracker is a CLI app to track your tasks and manage your to-do list.

## Features available
1. Add, Update, and Delete tasks
2. Mark a task as in progress or done
3. List all tasks
4. List all tasks that are done
5. List all tasks that are not done
6. List all tasks that are in progress

## Sample usages
1. Adding a new task
`$ task-tracker.py add "Buy groceries"`
`Output: Added new task with id = 1`

2. Updating and deleting tasks
`$ task-tracker.py update 1 "Buy groceries and cook dinner"`
`$ task-tracker.py delete 1`

3. Mark a task as in-progress or done
`$ task-tracker.py mark 1 in_progress`
`$ task-tracker.py mark 1 done`

4. Listing all tasks
`$ task-tracker.py list`

5. Listing tasks by status
`$ task-tracker.py list done`
`$ task-tracker.py list in_progress`
`$ task-tracker.py list todo`

