import tkinter as tk
from tkinter import ttk

def calculate():
    try:
        num1 = float(so1_entry.get())
        num2 = float(so2_entry.get())
        result_label.config(text=f"Kết quả: {num1 + num2}")
    except ValueError:
        result_label.config(text="Nhập số hợp lệ!")

root = tk.Tk()
root.geometry("240x150")
root.title('Tính')
root.resizable(0, 0)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)

so1_label = ttk.Label(root, text="Số 1: ")
so1_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
so1_entry = ttk.Entry(root)
so1_entry.grid(column=1, row=0, sticky=tk.E, padx=5, pady=5)

so2_label = ttk.Label(root, text="Số 2: ")
so2_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
so2_entry = ttk.Entry(root)
so2_entry.grid(column=1, row=1, sticky=tk.E, padx=5, pady=5)

tinh_button = ttk.Button(root, text="Tính", command=calculate)
tinh_button.grid(column=1, row=2, sticky=tk.E, padx=5, pady=5)

result_label = ttk.Label(root, text="")
result_label.grid(column=0, row=3, columnspan=2, pady=10)

root.mainloop()
