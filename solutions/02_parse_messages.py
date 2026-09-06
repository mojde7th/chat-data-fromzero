# -*- coding: utf-8 -*-
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
"""02 — پارس پیام‌ها با canon و flush."""
import re
from pathlib import Path

path = Path(__file__).resolve().parent.parent / "data" / "practice_chat.txt"
raw = path.read_text(encoding="utf-8")

HEADER = re.compile(
    r"^(.+?),\s*\[(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2})\]\s*$"
)

SKIP_BODY = {
    "❤",
    "👍",
    "In reply to this message",
}


def canon(name: str) -> str:
    """اسم نمایشی خام را به یک اسم رسمی یکتا تبدیل می‌کند."""
    s = name.strip()
    low = s.lower()
    # دو نفر جدا — قاطی نکن
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
    """پیام فعلی را اگر بدنهٔ معتبر دارد به لیست اضافه کن و خالی کن."""
    global cur
    if cur is None:
        return
    body = "\n".join(cur["body_lines"]).strip()
    if body and body not in SKIP_BODY:
        messages.append(
            {
                "who": cur["who"],
                "date": cur["date"],
                "time": cur["time"],
                "text": body,
            }
        )
    cur = None


for line in raw.splitlines():
    m = HEADER.match(line)
    if m:
        flush()
        cur = {
            "who": canon(m.group(1)),
            "date": m.group(2),
            "time": m.group(3),
            "body_lines": [],
        }
        continue
    if cur is None:
        continue
    if line.strip() == "":
        continue
    cur["body_lines"].append(line)

flush()

print("messages:", len(messages))
for msg in messages[:8]:
    preview = msg["text"].replace("\n", " ")[:40]
    print(f"{msg['time']} | {msg['who']} | {preview}")
