"""Filter using YYYY-MM-DD dates and an optional category."""
from expenses import print_expenses
from datetime import date

def filter_expenses(records):
    print("Leave a filter blank to include all values.")
    start = input("Start date YYYY-MM-DD: ").strip()
    end = input("End date YYYY-MM-DD: ").strip()
    category = input("Category: ").strip().lower()
    print_expenses(select_expenses(records, start, end, category))


def select_expenses(records, start="", end="", category=""):
    start, end = start.strip(), end.strip()
    category = category.strip().lower()
    for boundary in [start, end]:
        if boundary and date.fromisoformat(boundary).isoformat() != boundary:
            raise ValueError("Filter dates must use YYYY-MM-DD.")
    if start and end and start > end:
        raise ValueError("Start date must be on or before end date.")
    selected = []
    for row in records:
        if start and row[0] < start:
            continue
        if end and row[0] > end:
            continue
        if category and row[1].strip().lower() != category:
            continue
        selected.append(row)
    return selected
