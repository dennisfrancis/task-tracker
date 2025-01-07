#!/usr/bin/env python

"""Formatting functions for system objects"""

def fmt_list_of_strings(strlst: list[str]) -> str:
    """Formats a list of strings such that there are no quotation marks around the items."""
    return "[{}]".format(', '.join(strlst))
