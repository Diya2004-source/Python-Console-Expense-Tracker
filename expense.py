import sqlite3
from datetime import datetime

class ExpenseTracker:
    def __init__(self):
        self.con = sqlite3.connect("data/expenses.db") 
        self.create_table()

    def create_table(self):
        self.con.execute('''CREATE TABLE IF NOT EXISTS expenses
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             date TEXT,
                             category TEXT,
                             amount REAL,
                             note TEXT)''')   
        self.con.commit()

    def add_expense(self):
        date = input("Enter date (YYYY-MM-DD): ") or datetime.now().strftime("%Y-%m-%d")
        category = input("Enter category: ")
        amount = float(input("Enter amount: "))
        note = input("Enter note:  ")

        self.con.execute("INSERT INTO expenses (date,category,amount,note) VALUES (?,?,?,?)", 
                         (date, category, amount, note))
        self.con.commit()
        print(" Expense added successfully!")

    def view_expense(self):
        cursor = self.con.execute("SELECT * FROM expenses")
        print(" All Expenses:")
        for row in cursor:
            print(row)
        print()

    def monthly_summary(self):
        cursor = self.con.execute('''SELECT substr(date,1,7) AS month, SUM(amount)
                                     FROM expenses GROUP BY month''')
        print(" Monthly Summary:")
        for month, total in cursor:
            print(f"{month} → ₹{total}")
        print()

    def run(self):
        while True:
            print("\n1. Add Expense\n2. View Expenses\n3. Monthly Summary\n4. Exit")
            choice = input("Enter choice: ")
            if choice == '1':
                self.add_expense()
            elif choice == '2':
                self.view_expense()
            elif choice == '3':
                self.monthly_summary()
            elif choice == '4':
                print(" Goodbye!")
                break
            else:
                print(" Invalid choice!")

if __name__ == "__main__":
    ExpenseTracker().run()
