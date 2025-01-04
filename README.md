# Task tracker
Task-tracker is a CLI offline app to track your tasks and manage your to-do list.

## Features available
- [x] Add, Update, and Delete tasks
- [x] Mark a task as in progress or done
- [x] List all tasks
- [x] List all tasks that are done
- [x] List all tasks that are not done
- [x] List all tasks that are in progress

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

