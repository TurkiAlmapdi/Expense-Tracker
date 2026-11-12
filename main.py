from expenses import add_expense, print_expenses
from filters import filter_expenses
from storage import save_expenses, load_expenses
from csv_export import export_csv
def main():
    records = []
    while True:
        print("\n1 Add | 2 Print | 3 Filter | 4 Save | 5 Load | 6 CSV | 7 Quit")
        choice = input("Choose: ").strip()
        try:
            if choice == "1": add_expense(records)
            elif choice == "2": print_expenses(records)
            elif choice == "3": filter_expenses(records)
            elif choice == "4": save_expenses(records)
            elif choice == "5": records = load_expenses(records)
            elif choice == "6": export_csv(records)
            elif choice == "7": break
            else: print("Choose a number from 1 to 7.")
        except (OSError, ValueError) as error: print("Error:", error)
if __name__ == "__main__":
    import sys
    if "--console" in sys.argv:
        main()
    else:
        from interface import run
        run()
