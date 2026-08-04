#!/usr/bin/env python3
"""Connect to Microsoft To Do via Microsoft Graph (Device Code flow) and add today's tasks."""
import os, sys, json
from msal import PublicClientApplication, SerializableTokenCache
from requests import get, post

CLIENT_ID = "04b07795-8ddb-461a-bbee-02f9e1bf7b46"  # Azure CLI first-party public client
AUTHORITY = "https://login.microsoftonline.com/common"
SCOPES = ["https://graph.microsoft.com/Tasks.ReadWrite"]
CACHE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "todo_token_cache.bin")
GRAPH = "https://graph.microsoft.com/v1.0"

TASKS = [
    "☕ قهوة/شاي على البلكونة ونسمة الصبح الهادية",
    "🏃 ٣٠ دقيقة إليبتكال (قبل ما يسخن الجو)",
    "🍳 تجهيز أكلة جديدة بسيطة لنهاردة (من غير بحريات)",
    "🎬 فيلم أو سلسلة هادية من نوع مش بتشوفه عادة",
    "📖 قراءة أو كتاب صوتي وأنت قاعد مرتاح",
    "🕯️ روتين سبا بيتي هادي (شمعة + موسيقى هادية) بعد المغرب",
    "🌙 تأمل أو كتابة يومية في الـ vault قبل النوم",
]

cache = SerializableTokenCache()
if os.path.exists(CACHE_PATH):
    cache.deserialize(open(CACHE_PATH, "r").read())
app = PublicClientApplication(CLIENT_ID, authority=AUTHORITY, token_cache=cache)

accounts = app.get_accounts()
result = None
if accounts:
    result = app.acquire_token_silent(SCOPES, account=accounts[0])

if not result:
    flow = app.initiate_device_flow(SCOPES)
    if "error" in flow:
        print("DEVICE_FLOW_ERROR:", json.dumps(flow, ensure_ascii=False))
        sys.exit(1)
    print("=== AUTHENTICATE ===")
    print(flow["message"])
    print("=== END AUTH ===")
    sys.stdout.flush()
    result = app.acquire_token_by_device_flow(flow)

if "access_token" not in result:
    print("AUTH_FAILED:", json.dumps(result, ensure_ascii=False))
    sys.exit(1)

with open(CACHE_PATH, "w") as f:
    f.write(cache.serialize())

token = result["access_token"]
hdr = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# Get the "My Day" task list
lists_resp = get(f"{GRAPH}/me/todo/lists", headers=hdr).json()
lists = {l["displayName"]: l["id"] for l in lists_resp.get("value", [])}
print("LISTS:", json.dumps(lists, ensure_ascii=False))

# "My Day" is a special list; we find it by well-known name if present, else default "Tasks"
myday_id = lists.get("My Day") or lists.get("Tasks")
if not myday_id:
    print("NO_LIST_FOUND")
    sys.exit(1)

created = []
for t in TASKS:
    r = post(f"{GRAPH}/me/todo/lists/{myday_id}/tasks", headers=hdr,
             json={"title": t})
    if r.status_code in (200, 201):
        created.append(t)
        print("CREATED:", t)
    else:
        print("FAIL:", r.status_code, r.text[:200])

print(f"DONE: {len(created)}/{len(TASKS)} tasks created")
