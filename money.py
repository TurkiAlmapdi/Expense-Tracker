"""Store amounts as whole cents so totals stay exact."""

def read_cents(text):
    parts = text.strip().split(".")
    if len(parts) > 2:
        raise ValueError("Use an amount such as 12.50.")
    for part in parts:
        if not part.isascii() or not part.isdigit():
            raise ValueError("Enter digits, with an optional decimal point.")
    fraction = "00"
    if len(parts) == 2:
        if len(parts[1]) > 2:
            raise ValueError("Use at most two decimal places.")
        fraction = parts[1].ljust(2, "0")
    cents = int(parts[0]) * 100 + int(fraction)
    if cents == 0:
        raise ValueError("Enter an amount greater than zero.")
    return cents
def format_cents(cents):
    return f"{cents // 100}.{cents % 100:02d}"
