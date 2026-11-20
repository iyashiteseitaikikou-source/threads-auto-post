#!/usr/bin/env python3
import os
import json
import glob
import requests
from datetime import datetime
import pytz

ACCESS_TOKEN = os.environ["THREADS_ACCESS_TOKEN"]
USER_ID = os.environ["THREADS_USER_ID"]
TIME_SLOT = os.environ["TIME_SLOT"]  # "07", "12", "21"

JST = pytz.timezone("Asia/Tokyo")
today = datetime.now(JST).strftime("%Y-%m-%d")

post_text = None
for path in sorted(glob.glob("posts/*.json")):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if today in data and TIME_SLOT in data[today]:
        post_text = data[today][TIME_SLOT]
        break

if not post_text:
    print(f"投稿なし: {today} {TIME_SLOT}時")
    exit(0)

base_url = f"https://graph.threads.net/v1.0/{USER_ID}"

res = requests.post(f"{base_url}/threads", data={
    "media_type": "TEXT",
    "text": post_text,
    "access_token": ACCESS_TOKEN,
})
if not res.ok:
    print(f"APIエラー詳細: {res.text}")
res.raise_for_status()
container_id = res.json()["id"]

res2 = requests.post(f"{base_url}/threads_publish", data={
    "creation_id": container_id,
    "access_token": ACCESS_TOKEN,
})
res2.raise_for_status()

print(f"投稿完了: {today} {TIME_SLOT}時 → ID: {res2.json()['id']}")
