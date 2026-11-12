"""Save and load expense lists using JSON files."""
import json
from validation import check_records

def save_expenses(records, filename=None):
    if filename is None:
        filename = input("Save filename, for example expenses.json: ").strip()
        if input("Save and replace this file if it exists? y/n: ") != "y":
            return
    with open(filename, "w", encoding="utf-8") as file:
        file.write(json.dumps(records, indent=2))
    print("Expenses saved.")

def load_expenses(current, filename=None):
    if filename is None:
        if input("Replace current expenses? Save first. y/n: ") != "y":
            return current
        filename = input("JSON filename to open: ").strip()
    with open(filename, "r", encoding="utf-8") as file:
        records = check_records(json.loads(file.read()))
    print("Expenses loaded.")
    return records
