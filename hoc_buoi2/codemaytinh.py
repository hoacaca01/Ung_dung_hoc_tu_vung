from tkinter import *
import tkinter as tk

def press(key):
    current = entry.get()
    entry.delete(0, tk.END)
    entry.insert(0, current + key)

def calculate():
    try:
        expression = entry.get()
        result = eval(expression)
        entry.delete(0, tk.END)
        entry.insert(0, str(result))
    except Exception as e:
        entry.delete(0, tk.END)
        entry.insert(0, "Lỗi")


def clear():
    entry.delete(0, tk.END)

root = tk.Tk()
root.title("Máy Tính iPhone Hòa")

root.configure(bg="black")
text_input = StringVar()
entry = tk.Entry(root, width=30, font=("arial", 24, 'bold'), textvariable=text_input, bd=30, bg="black", fg="white", insertwidth=4, justify='right')
entry.grid(columnspan=4)

#btAC=Button(root, padx=20, bd=5, fg='black', font=("arial", 24, 'bold'), text='AC', bg='silver').grid(row=1, column=0)
#btCT=Button(root, padx=20, bd=5, fg='black', font=("arial", 24, 'bold'), text='+/-', bg='silver').grid(row=1, column=1)
#btPT=Button(root, padx=20, bd=5, fg='black', font=("arial", 24, 'bold'), text='%', bg='silver').grid(row=1, column=2)
#btChia=Button(root, padx=20, bd=5, fg='white', font=("arial", 24, 'bold'), text='÷', bg='orange').grid(row=1, column=3)
# ------------------------------------------------------------------------------------------------------
btC_frame = tk.Canvas(root, width=80, height=80, bg="black", highlightthickness=0)
btC_frame.grid(row=1, column=0)
btC_frame.create_oval(10, 10, 70, 70, fill="gray")
btC_text = btC_frame.create_text(40, 40, text='C', font=("arial", 24, 'bold'), fill="black")
btC_frame.bind("<Button-1>", lambda event: clear())

btCT_frame = tk.Canvas(root, width=80, height=80, bg="black", highlightthickness=0)
btCT_frame.grid(row=1, column=1)
btCT_frame.create_oval(10, 10, 70, 70, fill="gray")
btCT_text = btCT_frame.create_text(40, 40, text='+/-', font=("arial", 24, 'bold'), fill="black")

btPT_frame = tk.Canvas(root, width=80, height=80, bg="black", highlightthickness=0)
btPT_frame.grid(row=1, column=2)
btPT_frame.create_oval(10, 10, 70, 70, fill="gray")
btPT_text = btPT_frame.create_text(40, 40, text='%', font=("arial", 24, 'bold'), fill="black")


btChia_frame = tk.Canvas(root, width=80, height=80, bg="black", highlightthickness=0)
btChia_frame.grid(row=1, column=3)
btChia_frame.create_oval(10, 10, 70, 70, fill="orange")
btChia_text = btChia_frame.create_text(40, 40, text='÷', font=("arial", 24, 'bold'), fill="white")
btChia_frame.bind("<Button-1>", lambda event, key='/': press(key))
# ------------------------------------------------------------------------------------------------------

btTen = Button(root, width=20, padx=50, bd=5, fg='black', font=("arial", 24, 'bold'), text='PHẠM XUÂN HÒA', bg='silver')
btTen.grid(row=2, column=0, columnspan=4)
# btTen.bind("<Button-1>", lambda event, key='PHẠM XUÂN HÒA': press(key))

# ------------------------------------------------------------------------------------------------------
bt7_frame = tk.Canvas(root, width=80, height=80, bg="black", highlightthickness=0)
bt7_frame.grid(row=3, column=0)
bt7_frame.create_oval(10, 10, 70, 70, fill="gray")
bt7_text = bt7_frame.create_text(40, 40, text='7', font=("arial", 24, 'bold'), fill="black")
bt7_frame.bind("<Button-1>", lambda event, key='7': press(key))

bt8_frame = tk.Canvas(root, width=80, height=80, bg="black", highlightthickness=0)
bt8_frame.grid(row=3, column=1)
bt8_frame.create_oval(10, 10, 70, 70, fill="gray")
bt8_text = bt8_frame.create_text(40, 40, text='8', font=("arial", 24, 'bold'), fill="black")
bt8_frame.bind("<Button-1>", lambda event, key='8': press(key))

bt9_frame = tk.Canvas(root, width=80, height=80, bg="black", highlightthickness=0)
bt9_frame.grid(row=3, column=2)
bt9_frame.create_oval(10, 10, 70, 70, fill="gray")
bt9_text = bt9_frame.create_text(40, 40, text='9', font=("arial", 24, 'bold'), fill="black")
bt9_frame.bind("<Button-1>", lambda event, key='9': press(key))

btNhan_frame = tk.Canvas(root, width=80, height=80, bg="black", highlightthickness=0)
btNhan_frame.grid(row=3, column=3)
btNhan_frame.create_oval(10, 10, 70, 70, fill="orange")
btNhan_text = btNhan_frame.create_text(40, 40, text='x', font=("arial", 24, 'bold'), fill="white")
btNhan_frame.bind("<Button-1>", lambda event, key='*': press(key))
# ------------------------------------------------------------------------------------------------------
bt4_frame = tk.Canvas(root, width=80, height=80, bg="black", highlightthickness=0)
bt4_frame.grid(row=4, column=0)
bt4_frame.create_oval(10, 10, 70, 70, fill="gray")
bt4_text = bt4_frame.create_text(40, 40, text='4', font=("arial", 24, 'bold'), fill="black")
bt4_frame.bind("<Button-1>", lambda event, key='4': press(key))

bt5_frame = tk.Canvas(root, width=80, height=80, bg="black", highlightthickness=0)
bt5_frame.grid(row=4, column=1)
bt5_frame.create_oval(10, 10, 70, 70, fill="gray")
bt5_text = bt5_frame.create_text(40, 40, text='5', font=("arial", 24, 'bold'), fill="black")
bt5_frame.bind("<Button-1>", lambda event, key='5': press(key))

bt6_frame = tk.Canvas(root, width=80, height=80, bg="black", highlightthickness=0)
bt6_frame.grid(row=4, column=2)
bt6_frame.create_oval(10, 10, 70, 70, fill="gray")
bt6_text = bt6_frame.create_text(40, 40, text='6', font=("arial", 24, 'bold'), fill="black")
bt6_frame.bind("<Button-1>", lambda event, key='6': press(key))

btTru_frame = tk.Canvas(root, width=80, height=80, bg="black", highlightthickness=0)
btTru_frame.grid(row=4, column=3)
btTru_frame.create_oval(10, 10, 70, 70, fill="orange")
btTru_text = btTru_frame.create_text(40, 40, text='-', font=("arial", 24, 'bold'), fill="white")
btTru_frame.bind("<Button-1>", lambda event, key='-': press(key))
# ------------------------------------------------------------------------------------------------------
bt1_frame = tk.Canvas(root, width=80, height=80, bg="black", highlightthickness=0)
bt1_frame.grid(row=5, column=0)
bt1_frame.create_oval(10, 10, 70, 70, fill="gray")
bt1_text = bt1_frame.create_text(40, 40, text='1', font=("arial", 24, 'bold'), fill="black")
bt1_frame.bind("<Button-1>", lambda event, key='1': press(key))

bt2_frame = tk.Canvas(root, width=80, height=80, bg="black", highlightthickness=0)
bt2_frame.grid(row=5, column=1)
bt2_frame.create_oval(10, 10, 70, 70, fill="gray")
bt2_text = bt2_frame.create_text(40, 40, text='2', font=("arial", 24, 'bold'), fill="black")
bt2_frame.bind("<Button-1>", lambda event, key='2': press(key))

bt3_frame = tk.Canvas(root, width=80, height=80, bg="black", highlightthickness=0)
bt3_frame.grid(row=5, column=2)
bt3_frame.create_oval(10, 10, 70, 70, fill="gray")
bt3_text = bt3_frame.create_text(40, 40, text='3', font=("arial", 24, 'bold'), fill="black")
bt3_frame.bind("<Button-1>", lambda event, key='3': press(key))

btCong_frame = tk.Canvas(root, width=80, height=80, bg="black", highlightthickness=0)
btCong_frame.grid(row=5, column=3)
btCong_frame.create_oval(10, 10, 70, 70, fill="orange")
btCong_text = btCong_frame.create_text(40, 40, text='+', font=("arial", 24, 'bold'), fill="white")
btCong_frame.bind("<Button-1>", lambda event, key='+': press(key))
# ------------------------------------------------------------------------------------------------------
bt0_frame = tk.Canvas(root, width=80, height=80, bg="black", highlightthickness=0)
bt0_frame.grid(row=6, column=0)
bt0_frame.create_oval(10, 10, 70, 70, fill="gray")
bt0_text = bt0_frame.create_text(40, 40, text='0', font=("arial", 24, 'bold'), fill="black")
bt0_frame.bind("<Button-1>", lambda event, key='0': press(key))

btPhay_frame = tk.Canvas(root, width=80, height=80, bg="black", highlightthickness=0)
btPhay_frame.grid(row=6, column=2)
btPhay_frame.create_oval(10, 10, 70, 70, fill="gray")
btPhay_text = btPhay_frame.create_text(40, 40, text=',', font=("arial", 24, 'bold'), fill="black")
btPhay_frame.bind("<Button-1>", lambda event, key='.': press(key))

btBang_frame = tk.Canvas(root, width=80, height=80, bg="black", highlightthickness=0)
btBang_frame.grid(row=6, column=3)
btBang_frame.create_oval(10, 10, 70, 70, fill="orange")
btBang_text = btBang_frame.create_text(40, 40, text='=', font=("arial", 24, 'bold'), fill="white")
btBang_frame.bind("<Button-1>", lambda event, key='=': calculate())

root.mainloop()
