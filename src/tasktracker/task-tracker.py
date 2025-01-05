#!/usr/bin/env python

"""\
task-tracker is cli app to track and manage your tasks.
"""

__author__ = "Dennis Francis"
__credits__ = ["Dennis Francis"]
__license__ = "GPL"
__version__ = "0.1.0"
__maintainer__ = "Dennis Francis"
__email__ = "dennisfrancis.in@gmail.com"


import sys
from .cmdline import get_action, show_usage
from .tasks import TasksManager


def main():
    action = get_action(sys.argv, show_help=True)
    if action is None:
        show_usage()
        sys.exit(1)

    tm = TasksManager()
    tm.execute(action=action)


if __name__ == "__main__":
    main()

