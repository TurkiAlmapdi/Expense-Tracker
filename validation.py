"""Check expense data loaded from a JSON file."""
from datetime import date

def check_records(records):
    if not isinstance(records, list):
        raise ValueError("The file must contain a list of expenses.")
    for row in records:
        if not isinstance(row, list) or len(row) != 4:
            raise ValueError("Each expense must have four values.")
        day, category, note, cents = row
        if not isinstance(day, str):
            raise ValueError("The date must be text.")
        if date.fromisoformat(day).isoformat() != day:
            raise ValueError("Dates must use YYYY-MM-DD.")
        for text in [category, note]:
            if not isinstance(text, str) or not text.strip():
                raise ValueError("Category and description must contain text.")
        if type(cents) != int or cents <= 0:
            raise ValueError("The amount must be a positive integer in cents.")
    return records