from tkinter import *
from tkinter import messagebox

top = Tk()
top.geometry("400x200")


def clickRedButton():
    messagebox.showinfo("Hello", "Red Button clicked")


def clickBlueButton():
    messagebox.showinfo("Hello", "Blue Button clicked")

def clickGreenButton():
    messagebox.showinfo("Xanh", "Green Button clicked")

def clickYellowButton():
    messagebox.showinfo("Vang", "Yellow Button clicked")

b1 = Button(top, text="Red", command=clickRedButton, activeforeground="red", activebackground="yellow", pady=50)
b2 = Button(top, text="Blue", command=clickBlueButton, activeforeground="blue", activebackground="red", pady=40)
b3 = Button(top, text="Green", command=clickGreenButton, activeforeground="green", activebackground="yellow", pady=30)
b4 = Button(top, text="Yellow", command=clickYellowButton, activeforeground="yellow", activebackground="green", pady=20)
b1.pack(side=LEFT)
b2.pack(side=RIGHT)
b3.pack(side=TOP)
b4.pack(side=BOTTOM)
top.mainloop()