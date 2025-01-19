import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import json
import random
import os

data_file = ".accounts.json"

if os.path.exists(data_file):
    with open(data_file, "r") as file:
        accounts = json.load(file)
else:
    accounts = {}


def save_accounts():
    with open(data_file, "w") as file:
        json.dump(accounts, file)


def generate_account_number():
    while True:
        account_number = str(random.randint(100000, 999999))
        if account_number not in accounts:
            return account_number


def create_account():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Create Account", font=("Arial", 16)).pack(pady=10)
    tk.Label(root, text="Enter Account Holder Name:").pack()
    name_entry = tk.Entry(root, width=30)
    name_entry.pack(pady=5)

    def save_account():
        name = name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Name cannot be empty!")
            return

        account_number = generate_account_number()
        accounts[account_number] = {
            "name": name,
            "balance": 0,
            "log": [],
        }
        save_accounts()
        messagebox.showinfo("Success", f"Account created successfully!\nAccount Number: {account_number}")
        show_main_menu()

    tk.Button(root, text="Save", command=save_account).pack(pady=10)
    tk.Button(root, text="Back", command=show_main_menu).pack(pady=5)


def view_account(account_number=None):
    for widget in root.winfo_children():
        widget.destroy()

    if not account_number:
        tk.Label(root, text="View Account", font=("Arial", 16)).pack(pady=10)
        tk.Label(root, text="Enter Account Number:").pack()
        account_entry = tk.Entry(root, width=30)
        account_entry.pack(pady=5)

        def view_account_details():
            entered_account_number = account_entry.get().strip()
            if entered_account_number not in accounts:
                messagebox.showerror("Error", "Account not found!")
                return
            view_account(entered_account_number)

        tk.Button(root, text="View", command=view_account_details).pack(pady=10)
        tk.Button(root, text="Back", command=show_main_menu).pack(pady=5)
        return

    account_data = accounts[account_number]
    tk.Label(root, text=f"Account Holder: {account_data['name']}", font=("Arial", 14)).pack(pady=5)
    tk.Label(root, text=f"Account Number: {account_number}").pack(pady=5)
    balance_label = tk.Label(root, text=f"Balance: ₹{account_data['balance']}")
    balance_label.pack(pady=10)

    def update_balance_label():
        balance_label.config(text=f"Balance: ₹{accounts[account_number]['balance']}")

    def log_transaction(type_, amount):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        accounts[account_number]["log"].append({"type": type_, "amount": amount, "time": now})
        save_accounts()

    def deposit_money():
        amount = deposit_entry.get().strip()
        if not amount.isdigit() or int(amount) <= 0:
            messagebox.showerror("Error", "Enter a valid amount!")
            return

        amount = int(amount)
        accounts[account_number]["balance"] += amount
        log_transaction("Deposit", amount)
        messagebox.showinfo("Success", f"Deposited ₹{amount} successfully!")
        update_balance_label()

    def withdraw_money():
        amount = withdraw_entry.get().strip()
        if not amount.isdigit() or int(amount) <= 0:
            messagebox.showerror("Error", "Enter a valid amount!")
            return

        amount = int(amount)
        if amount > accounts[account_number]["balance"]:
            messagebox.showerror("Error", "Insufficient balance!")
            return

        accounts[account_number]["balance"] -= amount
        log_transaction("Withdraw", amount)
        messagebox.showinfo("Success", f"Withdrew ₹{amount} successfully!")
        update_balance_label()

    def view_log():
        for widget in root.winfo_children():
            widget.destroy()

        tk.Label(root, text=f"Transaction Log for {account_data['name']}", font=("Arial", 16)).pack(pady=10)
        log_data = accounts[account_number]["log"]
        if not log_data:
            tk.Label(root, text="No transactions yet.").pack(pady=10)
        else:
            for log_entry in log_data:
                tk.Label(root, text=f"{log_entry['time']} - {log_entry['type']}: ₹{log_entry['amount']}").pack(anchor="w", padx=20)

        tk.Button(root, text="Back", command=lambda: view_account(account_number)).pack(pady=10)

    tk.Label(root, text="Deposit Amount:").pack()
    deposit_entry = tk.Entry(root, width=20)
    deposit_entry.pack(pady=5)
    tk.Button(root, text="Deposit", command=deposit_money).pack(pady=5)

    tk.Label(root, text="Withdraw Amount:").pack()
    withdraw_entry = tk.Entry(root, width=20)
    withdraw_entry.pack(pady=5)
    tk.Button(root, text="Withdraw", command=withdraw_money).pack(pady=5)

    tk.Button(root, text="View Log", command=view_log).pack(pady=10)
    tk.Button(root, text="Back", command=show_main_menu).pack(pady=10)


def show_main_menu():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Bank Management System", font=("Arial", 18)).pack(pady=10)
    tk.Button(root, text="Create Account", command=create_account).pack(pady=10)
    tk.Button(root, text="View Account", command=view_account).pack(pady=10)
    tk.Button(root, text="Exit", command=root.quit).pack(pady=10)


root = tk.Tk()
root.title("Bank Management System")
root.geometry("500x400")

show_main_menu()
root.mainloop()
