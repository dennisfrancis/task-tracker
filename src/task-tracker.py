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
from cmdline import get_params, show_usage
from tasks import TasksManager


def main():
    params = get_params(sys.argv)
    if params is None:
        show_usage()
        sys.exit(1)

    tm = TasksManager()
    tm.execute(action=params.action, args=params.args)


if __name__ == "__main__":
    main()

