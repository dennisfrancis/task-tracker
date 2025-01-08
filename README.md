# Task tracker
Task-tracker is an offline CLI app to track your tasks and manage your to-do list.

![List of tasks in pretty tables](images/list.png)

## Features available
- [x] Add, update, and delete tasks
- [x] Mark a task as in progress or done
- [x] List all tasks
- [x] List all tasks that are done
- [x] List all tasks that are not done
- [x] List all tasks that are in progress
- [x] Ability to install using pip
- [x] Tasks display inside pretty tables

## Planned features
- Unit tests for TaskStore methods.
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

## How to run without installing?
First, clone the repo:
```
git clone https://github.com/dennisfrancis/task-tracker.git
```

Go into the src subfolder inside the project root:
```
cd task-tracker/src/
```

Run tasktracker's main entrypoint function with sub-commands like:
```
python3 -m tasktracker.tasktracker list # to list tasks.
python3 -m tasktracker.tasktracker add "Learn Typescript" # add new task.
```

