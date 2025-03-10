import tkinter as tk
from tkinter import messagebox
import requests  

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator and Currency Converter")
        self.root.geometry("400x400")

        # Calculator display
        self.display = tk.Entry(root, width=16, font=('Arial', 24), borderwidth=2, relief="solid")
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        # Calculator buttons
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', 'C', '=', '+'
        ]

        row_val = 1
        col_val = 0
        for button in buttons:
            tk.Button(root, text=button, width=5, height=2, command=lambda b=button: self.on_button_click(b)).grid(row=row_val, column=col_val, padx=5, pady=5)
            col_val += 1
            if col_val > 3:
                col_val = 0
                row_val += 1

        # Currency Converter UI
        tk.Label(root, text="Amount:").grid(row=5, column=0, padx=10, pady=10)
        tk.Label(root, text="From Currency:").grid(row=6, column=0, padx=10, pady=10)
        tk.Label(root, text="To Currency:").grid(row=7, column=0, padx=10, pady=10)
        tk.Label(root, text="Result:").grid(row=8, column=0, padx=10, pady=10)

        self.amount_entry = tk.Entry(root)
        self.amount_entry.grid(row=5, column=1, padx=10, pady=10)
        self.from_currency_entry = tk.Entry(root)
        self.from_currency_entry.grid(row=6, column=1, padx=10, pady=10)
        self.to_currency_entry = tk.Entry(root)
        self.to_currency_entry.grid(row=7, column=1, padx=10, pady=10)

        self.result_label = tk.Label(root, text="")
        self.result_label.grid(row=8, column=1, padx=10, pady=10)

        tk.Button(root, text="Convert", command=self.convert_currency).grid(row=9, column=0, padx=10, pady=10)
        tk.Button(root, text="Clear", command=self.clear_fields).grid(row=9, column=1, padx=10, pady=10)
        tk.Button(root, text="Exit", command=root.quit).grid(row=10, column=1, padx=10, pady=10)

    def on_button_click(self, char):
        if char == '=':
            try:
                result = eval(self.display.get())
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, str(result))
            except Exception as e:
                messagebox.showerror("Error", "Invalid input")
        elif char == 'C':
            self.display.delete(0, tk.END)
        else:
            self.display.insert(tk.END, char)

    def convert_currency(self):
        amount = self.amount_entry.get()
        from_currency = self.from_currency_entry.get().upper()
        to_currency = self.to_currency_entry.get().upper()

        if not amount or not from_currency or not to_currency:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Invalid amount. Please enter a numeric value.")
            return

        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
        response = requests.get(url)

        if response.status_code != 200:
            messagebox.showerror("Error", "Failed to fetch exchange rates. Please try again later.")
            return

        data = response.json()
        if to_currency not in data['rates']:
            messagebox.showerror("Error", f"Currency {to_currency} not found.")
            return

        rate = data['rates'][to_currency]
        converted_amount = amount * rate
        self.result_label.config(text=f"{amount} {from_currency} = {converted_amount:.2f} {to_currency}")

    def clear_fields(self):
        self.amount_entry.delete(0, tk.END)
        self.from_currency_entry.delete(0, tk.END)
        self.to_currency_entry.delete(0, tk.END)
        self.result_label.config(text="")
        self.display.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
    print("Calculator and Currency Converter application has been executed successfully.")
