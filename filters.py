"""Filter using YYYY-MM-DD dates and an optional category."""
from expenses import print_expenses

def filter_expenses(records):
    print("Leave a filter blank to include all values.")
    start = input("Start date YYYY-MM-DD: ").strip()
    end = input("End date YYYY-MM-DD: ").strip()
    category = input("Category: ").strip().lower()
    selected = []
    for row in records:
        if start and row[0] < start:
            continue
        if end and row[0] > end:
            continue
        if category and row[1].lower() != category:
            continue
        selected.append(row)
    if not selected:
        print("No matching expenses.")
    print_expenses(selected)