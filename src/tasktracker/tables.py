#!/usr/bin/env python

"""\
Helper functions for pretty printing list of tasks using tables.
"""

from typing import Dict, List

def _get_col_sizes(data: List[Dict[str, str]], columns: List[str], max_sizes: Dict[str, int]) -> List[int]:
    """Internal function to compute maximum length of each column.

    Keyword arguments:
    data      : a list of rows of data represented as a dictionary(key =
                column-name, value = cell-value).
    columns   : a list of column names.
    max_sizes : (Optional) dictionary containing maximum length of columns(key =
                column-name, value = maximum length of that column).

    returns a list of lengths representing the maximum length of each column.
    """
    col_sizes = [min(len(col), max_sizes[col] if col in max_sizes else len(col)) for col in columns]
    for row in data:
        for idx, col in enumerate(columns):
            col_sizes[idx] = max(col_sizes[idx], len(row[col]))
    for idx, col in enumerate(columns):
        if col in max_sizes:
            col_sizes[idx] = min(col_sizes[idx], max_sizes[col])
    return col_sizes

def _trim(row: List[str], max_col_lens: List[int]) -> List[str]:
    """Trims the cell values(strings) of the given row according to the specification of maximum column size.

    Keyword arguments:

    row: list of strings specifying a row of data from a table.
    max_col_lens: specifies the maximum size of each column.
    """
    for idx in range(len(row)):
        cell = row[idx]
        cell_max = max_col_lens[idx]
        if len(cell) > cell_max:
            row[idx] = cell[:cell_max - 3] + "..."
    return row

def _get_rows(data: List[Dict[str, str]], columns: List[str], max_col_lens: List[int]) -> List[List[str]]:
    """Internal function that transforms a list of dictionaries to list of lists(2D matrix of strings).

    The cell values are trimmed in length if they exceed the maximum length specified by max_col_lens.

    Keyword arguments:
    data: table data in the form of list of dicts of strings where keys are column names and values are cell values.
    columns: the column names.
    max_col_lens: a list that stores the maximum length of each column.

    returns the transformed data.
    """
    columns_trimmed = _trim(columns.copy(), max_col_lens)
    rows = [columns_trimmed,]
    for row_dict in data:
        row = _trim([row_dict[col] for col in columns], max_col_lens)
        rows.append(row)
    return rows

def _draw_table(rows: List[List[str]], max_col_lens: List[int]):
    """Internal implementation that renders a table.

    Keyword arguments:
    rows: A 2-D matrix of strings to be represented as a table in the console.
    max_col_lens: provides the maximum length of each column.
    """
    # print the table's top border
    print("┌" + "┬".join("─" * (n + 2) for n in max_col_lens) + "┐")
    rows_separator = "├" + "┼".join("─" * (n + 2) for n in max_col_lens) + "┤"
    header_separator = "╞" + "╪".join("═" * (n + 2) for n in max_col_lens) + "╡"
    row_fstring = " │ ".join("{: <%s}" % n for n in max_col_lens)
    bold_start = "\033[1m"
    bold_end = "\033[0m"
    header_fstring = " │ ".join((bold_start + "{: <%s}" + bold_end) % n for n in max_col_lens)

    for idx, row in enumerate(rows):
        row_str = header_fstring.format(*row) if idx == 0 else row_fstring.format(*row)
        print("│", row_str, "│")
        if idx < len(rows) - 1:
            if idx == 0:
                print(header_separator)
            else:
                print(rows_separator)


    # print the table's bottom border
    print("└" + "┴".join("─" * (n + 2) for n in max_col_lens) + "┘")

def show_table(data: List[Dict[str, str]], columns: List[str], max_sizes: Dict[str, int] = {}):
    """Displays the data in a pretty tabular form.

    Keyword arguments:
    data      : a list of rows of data represented as a dictionary(key =
                column-name, value = cell-value).
    columns   : a list of column names.
    max_sizes : (Optional) dictionary containing maximum length of columns(key =
                column-name, value = maximum length of that column).
    """
    max_col_lens = _get_col_sizes(data, columns, max_sizes)
    rows = _get_rows(data, columns, max_col_lens)
    _draw_table(rows, max_col_lens)

def _sample_run():
    """Function that shows a sample usage of show_table"""
    data = [
            { "Name": "XYZ", "Description" : "A Long description fdhjfks fdkshfksdj fkdshfkdsjs fkdshfkjdshfks" },
            { "Name": "LongNamefdshfkjsdhfkshfkshdkfhsfhksdhfkhsdkhfksfh", "Description": "short description"},]
    columns = ["Name", "Description"]
    max_sizes = {"Name": 10, "Description": 20}
    show_table(data, columns, max_sizes)

if __name__ == "__main__":
    _sample_run()

