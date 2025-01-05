# Task tracker
Task-tracker is a CLI offline app to track your tasks and manage your to-do list.

## Features available
- [x] Add, update, and delete tasks
- [x] Mark a task as in progress or done
- [x] List all tasks
- [x] List all tasks that are done
- [x] List all tasks that are not done
- [x] List all tasks that are in progress
- [x] Ability to install using pip 

## Planned features
- Show list of tasks in pretty tables (without any libraries)
    - [This](https://stackoverflow.com/a/77820161) might be a good starting point.
- Display the affected task after add/update/mark/delete execution in pretty table form.
- Unit tests for TaskStore methods.
- Docstrings for all classes and methods.
- Code structure documentation in README.

## How to install?
Task-tracker can be installed using pip like:
```
pip install git+https://github.com/dennisfrancis/task-tracker.git
```
**Note**: Sample usages below assume that you have installed the package using pip as shown above.

## Sample usages
1. Adding a new task
```
task-tracker add "Buy groceries"
task-tracker add "Do laundry"
task-tracker add "Finish this week's project"
task-tracker add "Practice guitar"
```

3. Updating and deleting tasks
```
task-tracker update 1 "Buy groceries and cook dinner"
task-tracker delete 1
```

3. Mark a task as in-progress or done
```
task-tracker mark 3 in_progress
task-tracker mark 2 done
```

4. Listing all tasks
```
task-tracker list
```

5. Listing tasks by status
```
task-tracker list done
task-tracker list in_progress
task-tracker list todo
```

