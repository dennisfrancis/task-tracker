#!/usr/bin/env python

"""Formatting functions for system objects"""

def fmt_list_of_strings(strlst: list[str]) -> str:
    return "[{}]".format(', '.join(strlst))
