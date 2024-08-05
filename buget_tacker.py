from expense import Expense
import calendar
import datetime
import os
from typing import List

def main():
    print("🎯 Running Expense Tracker!")
    expense_file_path = "expenses.csv"
    budget = 2000

    # Get user input for expense.
    expense = get_user_expense()

    # Write their expense to a file.
    save_expense_to_file(expense, expense_file_path)

    # Read file and summarize expenses.
    summarize_expenses(expense_file_path, budget)

def get_user_expense() -> Expense:
    print("🎯 Getting User Expense")
    expense_name = input("Enter expense name: ")

    while True:
        try:
            expense_amount_input = input("Enter expense amount: ")
            expense_amount = float(expense_amount_input)
            if expense_amount < 0:
                raise ValueError("Expense amount cannot be negative.")
            break
        except ValueError as e:
            print(f"Invalid input: {e}. Please enter a valid amount.")

    expense_categories = [
        "🍔 Food",
        "🏠 Home",
        "💼 Work",
        "🎉 Fun",
        "✨ Misc",
    ]

    while True:
        print("Select a category: ")
        for i, category_name in enumerate(expense_categories):
            print(f"  {i + 1}. {category_name}")

        value_range = f"[1 - {len(expense_categories)}]"
        try:
            selected_index = int(input(f"Enter a category number {value_range}: ")) - 1
            if 0 <= selected_index < len(expense_categories):
                selected_category = expense_categories[selected_index]
                return Expense(
                    name=expense_name, category=selected_category, amount=expense_amount
                )
            else:
                print("Invalid category. Please try again!")
        except ValueError:
            print("Invalid input. Please enter a number.")

def save_expense_to_file(expense: Expense, expense_file_path: str):
    print(f"🎯 Saving User Expense: {expense} to {expense_file_path}")
    try:
        with open(expense_file_path, "a", encoding="utf-8") as f:
            f.write(f"{expense.name},{expense.amount},{expense.category}\n")
    except IOError as e:
        print(f"Error saving expense: {e}")

def summarize_expenses(expense_file_path: str, budget: float):
    print("🎯 Summarizing User Expenses")

    if not os.path.exists(expense_file_path):
        print("No expenses recorded yet. Start adding your expenses!")
        return

    expenses: List[Expense] = []
    try:
        with open(expense_file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                expense_name, expense_amount, expense_category = line.strip().split(",")
                expenses.append(Expense(
                    name=expense_name,
                    amount=float(expense_amount),
                    category=expense_category,
                ))
    except IOError as e:
        print(f"Error reading expenses: {e}")
        return

    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount

    print("Expenses By Category 📈:")
    for key, amount in amount_by_category.items():
        print(f"  {key}: ${amount:.2f}")

    total_spent = sum(expense.amount for expense in expenses)
    print(f"💵 Total Spent: ${total_spent:.2f}")

    remaining_budget = budget - total_spent
    print(f"✅ Budget Remaining: ${remaining_budget:.2f}")

    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day

    if remaining_days > 0:
        daily_budget = remaining_budget / remaining_days
        print(green(f"👉 Budget Per Day: ${daily_budget:.2f}"))
    else:
        print("⚠️ No remaining days in this month!")

def green(text: str) -> str:
    return f"\033[92m{text}\033[0m"

if __name__ == "__main__":
    main()


