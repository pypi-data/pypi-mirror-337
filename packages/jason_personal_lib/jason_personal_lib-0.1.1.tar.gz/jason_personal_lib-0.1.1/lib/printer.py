import time
from wcwidth import wcswidth


def better_print_str(s: str, delay: float = 0.1) -> None:
    """
    Print the string character by character with a specified delay between each character.

    :param s: The string to print.
    :param delay: The delay in seconds between each character (default is 0.1 seconds).
    """
    for ch in s:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print()  # Print a newline after printing the string


def print_table(table: list):
    """
    Print table nicely.

    :param table: the table to print.
    """
    col_widths = []
    num_cols = len(table[0])
    for col in range(num_cols):
        max_width = max(wcswidth(str(row[col])) for row in table)
        col_widths.append(max_width)

    for row in table:
        formatted_row = " | ".join(
            str(cell).ljust(col_widths[i] - wcswidth(str(cell)) + len(str(cell)))
            for i, cell in enumerate(row)
        )
        print(formatted_row)
