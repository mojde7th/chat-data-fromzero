# -*- coding: utf-8 -*-
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
"""03 — شمارش پیام هر نفر بعد از canon."""
import collections
import re
from pathlib import Path

path = Path(__file__).resolve().parent.parent / "data" / "practice_chat.txt"
raw = path.read_text(encoding="utf-8")

HEADER = re.compile(
    r"^(.+?),\s*\[(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2})\]\s*$"
)
SKIP_BODY = {"❤", "👍", "In reply to this message"}


def canon(name: str) -> str:
    s = name.strip()
    low = s.lower()
    # دو هستی و دو سپیده جدا
    if s == "Hasti Arya" or "arya" in low:
        return "هستی آریا"
    if low == "hasti":
        return "هستی"
    if s == "SEPI":
        return "سپی"
    if low.startswith("sepide"):
        return "سپیده"
    if s == "Niaz":
        return "نیاز"
    if s == "Mojde":
        return "مژده"
    if "Tamjidi" in s:
        return "مهسا"
    if "Latifi" in s:
        return "یاسمن"
    if "Cani" in s:
        return "کانی"
    if s == "Monir":
        return "منیر"
    return s


messages = []
cur = None


def flush():
    global cur
    if cur is None:
        return
    body = "\n".join(cur["body_lines"]).strip()
    if body and body not in SKIP_BODY:
        messages.append({"who": cur["who"], "text": body})
    cur = None


for line in raw.splitlines():
    m = HEADER.match(line)
    if m:
        flush()
        cur = {"who": canon(m.group(1)), "body_lines": []}
        continue
    if cur is None or line.strip() == "":
        continue
    cur["body_lines"].append(line)
flush()

counts = collections.Counter(msg["who"] for msg in messages)
print("people:", len(counts))
for who, n in counts.most_common():
    print(f"{n:3d}  {who}")
