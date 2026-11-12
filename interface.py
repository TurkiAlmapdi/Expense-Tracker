"""Tkinter desktop interface for the expense tracker."""
from datetime import date
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from csv_export import export_csv
from filters import select_expenses
from money import format_cents, read_cents
from storage import load_expenses, save_expenses
from validation import check_records


class ExpenseWindow:
    def __init__(self, root):
        self.root = root
        self.records = []
        self.visible_records = []
        self.active_filters = ("", "", "")
        self.changed = False
        self.filename = None
        self.root.title("Expense Tracker")
        self.root.geometry("1060x720")
        self.root.minsize(900, 640)
        self.root.configure(bg="#f3f5f8")
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.style = ttk.Style(root)
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#f3f5f8")
        self.style.configure("TLabel", background="#f3f5f8", font=("Segoe UI", 10))
        self.style.configure("Title.TLabel", font=("Segoe UI", 24, "bold"))
        self.style.configure("Total.TLabel", font=("Segoe UI", 17, "bold"), foreground="#174ea6")
        self.style.configure("TButton", font=("Segoe UI", 10), padding=8)
        self.style.configure("Accent.TButton", background="#174ea6", foreground="white")
        self.style.map("Accent.TButton", background=[("active", "#123e84")])
        self.style.configure("Treeview", font=("Segoe UI", 10), rowheight=30)
        self.style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), padding=8)
        self.build_window()
        self.refresh()

    def labeled_entry(self, parent, label, column, value="", width=18):
        ttk.Label(parent, text=label).grid(row=0, column=column, sticky="w", pady=(0, 5))
        variable = tk.StringVar(self.root, value=value)
        entry = ttk.Entry(parent, textvariable=variable, width=width, font=("Segoe UI", 11))
        entry.grid(row=1, column=column, sticky="ew", padx=(0, 12), ipady=5)
        parent.columnconfigure(column, weight=1)
        return variable

    def build_window(self):
        page = ttk.Frame(self.root, padding=24)
        page.pack(fill="both", expand=True)
        ttk.Label(page, text="Expense Tracker", style="Title.TLabel").pack(anchor="w")
        ttk.Label(page, text="Record your spending. Find an expense. Keep a copy.").pack(anchor="w", pady=(4, 18))

        toolbar = ttk.Frame(page)
        toolbar.pack(fill="x", pady=(0, 18))
        ttk.Button(toolbar, text="Open JSON", command=self.open_file).pack(side="left", padx=(0, 8))
        ttk.Button(toolbar, text="Save JSON", command=self.save_file).pack(side="left", padx=(0, 8))
        ttk.Button(toolbar, text="Export shown rows to CSV", command=self.export_file).pack(side="left")
        self.file_text = tk.StringVar(self.root, value="New expense list")
        ttk.Label(toolbar, textvariable=self.file_text).pack(side="right")

        ttk.Label(page, text="ADD AN EXPENSE", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 8))
        form = ttk.Frame(page)
        form.pack(fill="x")
        self.day = self.labeled_entry(form, "Date (YYYY-MM-DD)", 0, date.today().isoformat())
        self.category = self.labeled_entry(form, "Category", 1)
        self.description = self.labeled_entry(form, "Description", 2, width=28)
        self.amount = self.labeled_entry(form, "Amount", 3, width=12)
        ttk.Button(form, text="Add expense", style="Accent.TButton", command=self.add).grid(row=1, column=4)

        ttk.Separator(page).pack(fill="x", pady=20)
        ttk.Label(page, text="FILTER EXPENSES", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 8))
        filters = ttk.Frame(page)
        filters.pack(fill="x")
        self.start = self.labeled_entry(filters, "From (YYYY-MM-DD)", 0)
        self.end = self.labeled_entry(filters, "To (YYYY-MM-DD)", 1)
        self.filter_category = self.labeled_entry(filters, "Category", 2)
        ttk.Button(filters, text="Apply filters", command=self.apply_filters).grid(row=1, column=3, padx=(0, 8))
        ttk.Button(filters, text="Clear", command=self.clear_filters).grid(row=1, column=4)
        ttk.Label(page, text="Leave filters blank to include all expenses. Date limits include both days.").pack(anchor="w", pady=(6, 12))

        table_frame = ttk.Frame(page)
        table_frame.pack(fill="both", expand=True)
        self.table = ttk.Treeview(table_frame, columns=("date", "category", "description", "amount"), show="headings")
        for name, heading, width in [("date", "Date", 135), ("category", "Category", 160),
                                     ("description", "Description", 380), ("amount", "Amount", 110)]:
            self.table.heading(name, text=heading)
            self.table.column(name, width=width, minwidth=80, anchor="e" if name == "amount" else "w")
        scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        self.table.pack(side="left", fill="both", expand=True)

        footer = ttk.Frame(page)
        footer.pack(fill="x", pady=(14, 0))
        self.count_text = tk.StringVar(self.root)
        self.total_text = tk.StringVar(self.root)
        ttk.Label(footer, textvariable=self.count_text).pack(side="left")
        ttk.Label(footer, textvariable=self.total_text, style="Total.TLabel").pack(side="right")
        self.status = tk.StringVar(self.root, value="Add your first expense or open a saved JSON file.")
        ttk.Label(page, textvariable=self.status, wraplength=950).pack(anchor="w", pady=(10, 0))

    def refresh(self):
        self.visible_records = select_expenses(self.records, *self.active_filters)
        for item in self.table.get_children():
            self.table.delete(item)
        for day, category, description, cents in self.visible_records:
            self.table.insert("", "end", values=(day, category, description, format_cents(cents)))
        self.count_text.set(f"Showing {len(self.visible_records)} of {len(self.records)} expenses")
        self.total_text.set("Shown total  " + format_cents(sum(row[3] for row in self.visible_records)))
        name = Path(self.filename).name if self.filename else "New expense list"
        self.file_text.set(name + (" • Unsaved changes" if self.changed else ""))

    def add(self):
        try:
            record = [self.day.get().strip(), self.category.get().strip(),
                      self.description.get().strip(), read_cents(self.amount.get())]
            check_records([record])
        except ValueError as error:
            messagebox.showerror("Check expense details", str(error), parent=self.root)
            return
        self.records.append(record)
        self.changed = True
        self.description.set("")
        self.amount.set("")
        self.refresh()
        self.status.set("Expense added. Save JSON to keep your changes. Active filters may hide this row.")

    def apply_filters(self):
        requested = (self.start.get(), self.end.get(), self.filter_category.get())
        try:
            select_expenses(self.records, *requested)
        except ValueError as error:
            messagebox.showerror("Check filters", str(error), parent=self.root)
            return
        self.active_filters = requested
        self.refresh()
        self.status.set("Filters applied." if self.visible_records else "No expenses match these filters.")

    def clear_filters(self):
        for variable in [self.start, self.end, self.filter_category]:
            variable.set("")
        self.active_filters = ("", "", "")
        self.refresh()
        self.status.set("Showing all expenses.")

    def save_file(self):
        filename = filedialog.asksaveasfilename(parent=self.root, title="Save all expenses",
                                               defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if not filename:
            return False
        try:
            save_expenses(self.records, filename)
        except (OSError, ValueError) as error:
            messagebox.showerror("Could not save", str(error), parent=self.root)
            return False
        self.filename = filename
        self.changed = False
        self.refresh()
        self.status.set("All expenses saved to " + filename)
        return True

    def confirm_changes(self):
        if not self.changed:
            return True
        answer = messagebox.askyesnocancel("Unsaved changes", "Save your expenses before continuing?", parent=self.root)
        if answer is None:
            return False
        if answer:
            return self.save_file()
        return True

    def open_file(self):
        filename = filedialog.askopenfilename(parent=self.root, title="Open expenses",
                                              filetypes=[("JSON files", "*.json")])
        if not filename:
            return
        try:
            loaded = load_expenses(self.records, filename)
        except (OSError, ValueError) as error:
            messagebox.showerror("Could not open", str(error), parent=self.root)
            return
        if not self.confirm_changes():
            return
        self.records = loaded
        self.filename = filename
        self.changed = False
        self.clear_filters()
        self.status.set("Opened " + filename)

    def export_file(self):
        filename = filedialog.asksaveasfilename(parent=self.root, title="Export shown expenses",
                                               defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not filename:
            return
        try:
            export_csv(self.visible_records, filename)
        except (OSError, ValueError) as error:
            messagebox.showerror("Could not export", str(error), parent=self.root)
            return
        self.status.set(f"Exported {len(self.visible_records)} shown expenses to {filename}. Save JSON to keep all records.")

    def close(self):
        if self.confirm_changes():
            self.root.destroy()


def run():
    root = tk.Tk()
    ExpenseWindow(root)
    root.mainloop()
