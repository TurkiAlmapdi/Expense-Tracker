"""Run the expense tracker with python main.py."""
from expenses import add_expense, print_expenses

def main():
    records = []
    print("Expenses stay in memory until you quit.")
    while True:
        print("\n1. Add expense     2. Print expenses     3. Filter expenses")
        print("4. Save JSON       5. Load JSON          6. Export CSV     7. Quit")
        choice = input("Choose: ").strip()
        if choice == "1":
            add_expense(records)
        elif choice == "2":
            print_expenses(records)
        elif choice == "7":
            break
        else:
            print("Choose 1, 2, or 7. Options 3 through 6 are planned.")
if __name__ == "__main__":
    main()
