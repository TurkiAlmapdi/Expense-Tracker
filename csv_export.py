"""Export expenses to a CSV file for Microsoft Excel."""
from money import format_cents

def export_csv(records, filename=None):
    interactive = filename is None
    if interactive:
        filename = input("CSV filename, for example expenses.csv: ").strip()
    if not filename:
        raise ValueError("Enter a filename.")
    if interactive and input("Export and replace this file if it exists? y/n: ") != "y":
        return
    with open(filename, "w", encoding="utf-8-sig", newline="") as file:
        file.write("Date,Category,Description,Amount\r\n")
        for expense in records:
            fields = []
            for text in expense[:3]:
                escaped = text.replace('"', '""')
                fields.append('"' + escaped + '"')
            fields.append(format_cents(expense[3]))
            line = ",".join(fields)
            file.write(line + "\r\n")
    print("CSV exported.")
