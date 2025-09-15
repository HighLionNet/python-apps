#! /usr/bin/env python

import random
import tkinter as tk
from tkinter import messagebox


def roll_dice():
    try:
        sides = int(sides_entry.get())
        count = int(count_entry.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers.")
        return

    results = [random.randint(1, sides) for _ in range(count)]
    result_label.config(text="You rolled: " + ", ".join(map(str, results)))


# --- GUI setup ---
root = tk.Tk()
root.title("Dice Roller")

# Labels and entries
tk.Label(root, text="Number of sides:").grid(row=0, column=0, padx=5, pady=5)
sides_entry = tk.Entry(root)
sides_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Number of dice:").grid(row=1, column=0, padx=5, pady=5)
count_entry = tk.Entry(root)
count_entry.grid(row=1, column=1, padx=5, pady=5)

# Roll button
roll_button = tk.Button(root, text="Roll!", command=roll_dice)
roll_button.grid(row=2, column=0, columnspan=2, pady=10)

# Result label
result_label = tk.Label(root, text="You rolled: ")
result_label.grid(row=3, column=0, columnspan=2, pady=5)

# Run the GUI loop
root.mainloop()
