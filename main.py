"""Expense tracker starter: menu only; other features are TODO."""

def main():
    while True:
        print("\nExpense Tracker")
        print("1. Add expense")
        print("2. Print expenses")
        print("3. Filter expenses")
        print("4. Save JSON")
        print("5. Load JSON")
        print("6. Export CSV")
        print("7. Quit")
        choice = input("Choose: ")
        if choice == "7":
            break
        else:
            print("TODO: this feature is not implemented.")

if __name__ == "__main__":
    main()
