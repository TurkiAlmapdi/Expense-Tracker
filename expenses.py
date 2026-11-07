from datetime import date
from money import read_cents, format_cents

def add_expense(records):
    try:
        day = input("Date YYYY-MM-DD: ").strip()
        if date.fromisoformat(day).isoformat() != day:
            raise ValueError("Use YYYY-MM-DD.")
        category = input("Category: ").strip()
        note = input("Description: ").strip()
        if not category or not note:
            raise ValueError("Enter a category and description.")
        records.append([day, category, note, read_cents(input("Amount: "))])
        print("Expense added.")
    except ValueError as error:
        print("Entry canceled.", error)
def print_expenses(records):
    for day, category, note, cents in records:
        print(f"{day} | {category} | {note} | {format_cents(cents)}")
    print("Total:", format_cents(sum(row[3] for row in records)))
