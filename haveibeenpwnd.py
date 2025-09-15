#! /usr/bin/env python

import hashlib
import requests
import re
import tkinter as tk
from tkinter import messagebox, ttk

HIBP_API_URL = "https://api.pwnedpasswords.com/range/{}"

def pwned_api_check(password: str) -> int:
    sha1 = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]
    try:
        res = requests.get(HIBP_API_URL.format(prefix))
        res.raise_for_status()
    except requests.RequestException:
        return -1
    hashes = (line.split(":") for line in res.text.splitlines())
    for h, count in hashes:
        if h == suffix:
            return int(count)
    return 0

def evaluate_password(pw: str):
    score = 0
    if len(pw) >= 8: score += 1
    if re.search(r"[a-z]", pw): score += 1
    if re.search(r"[A-Z]", pw): score += 1
    if re.search(r"\d", pw): score += 1
    if re.search(r"[@$!%*?&]", pw): score += 1
    verdicts = {0:"Very Weak",1:"Weak",2:"Weak",3:"Medium",4:"Strong",5:"Very Strong"}
    return score, verdicts.get(score, "Weak")

def check_strength():
    pw = entry.get()
    if not pw:
        messagebox.showwarning("Empty", "Please enter a password!")
        return
    score, verdict = evaluate_password(pw)

    # Progress bar update
    progress["value"] = score * 20
    colors = ["#ff5555", "#ffb86c", "#f1fa8c", "#50fa7b", "#00ff99"]
    verdict_label.config(text=f"Strength: {verdict} ({score}/5)",
                         fg=colors[min(score, len(colors)-1)])

    # HIBP check
    leaks = pwned_api_check(pw)
    if leaks > 0:
        breach_label.config(text=f"⚠️ Leaked: YES ({leaks} times)", fg="#ff5555")
    elif leaks == 0:
        breach_label.config(text="✔️ Leaked: NO", fg="#50fa7b")
    else:
        breach_label.config(text="❓ Error checking breach status", fg="#f1fa8c")

def toggle_password():
    entry.config(show="" if show_var.get() else "*")

def copy_password():
    pw = entry.get()
    if pw:
        root.clipboard_clear()
        root.clipboard_append(pw)
        messagebox.showinfo("Copied", "Password copied to clipboard!")

def reset_fields():
    entry.delete(0, tk.END)
    progress["value"] = 0
    verdict_label.config(text="Strength: N/A", fg="#f8f8f2")
    breach_label.config(text="", fg="#f8f8f2")

def animate_title():
    colors = ["#50fa7b", "#8be9fd", "#bd93f9", "#ff79c6"]
    current = animate_title.counter % len(colors)
    title_label.config(fg=colors[current])
    animate_title.counter += 1
    root.after(500, animate_title)
animate_title.counter = 0

# --- GUI Setup ---
root = tk.Tk()
root.title("⚡ Hacker Password Analyzer ⚡")
root.geometry("1000x600")
root.configure(bg="#282a36")

# Title with animation
title_label = tk.Label(root, text="HACKER PASSWORD ANALYZER",
                       font=("Consolas", 28, "bold"),
                       bg="#282a36", fg="#50fa7b")
title_label.pack(pady=20)

# Password input
tk.Label(root, text="Password:", font=("Consolas", 18),
         bg="#282a36", fg="#8be9fd").pack(anchor="w", padx=20, pady=10)

entry = tk.Entry(root, width=50, show="*", font=("Consolas", 18),
                 bg="#44475a", fg="#f8f8f2", insertbackground="#50fa7b")
entry.pack(padx=20, pady=10)

# Show toggle
show_var = tk.BooleanVar()
tk.Checkbutton(root, text="Show password", variable=show_var, command=toggle_password,
               font=("Consolas", 14), bg="#282a36", fg="#bd93f9",
               activebackground="#282a36", activeforeground="#bd93f9").pack(anchor="w", padx=20, pady=10)

# Buttons
btn_frame = tk.Frame(root, bg="#282a36")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Analyze", command=check_strength,
          font=("Consolas", 16), bg="#6272a4", fg="#f8f8f2").grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="Copy", command=copy_password,
          font=("Consolas", 16), bg="#6272a4", fg="#f8f8f2").grid(row=0, column=1, padx=10)
tk.Button(btn_frame, text="Reset", command=reset_fields,
          font=("Consolas", 16), bg="#6272a4", fg="#f8f8f2").grid(row=0, column=2, padx=10)

# Progress bar
progress = ttk.Progressbar(root, length=600, mode="determinate")
progress.pack(pady=20)

# Verdict and breach labels
verdict_label = tk.Label(root, text="Strength: N/A", font=("Consolas", 20),
                         bg="#282a36", fg="#f8f8f2")
verdict_label.pack(pady=10)

breach_label = tk.Label(root, text="", font=("Consolas", 18),
                        bg="#282a36", fg="#f8f8f2")
breach_label.pack(pady=10)

# Start animation
animate_title()

root.mainloop()
