# -*- coding: utf-8 -*-
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
"""04 — پرتکرارترین واژه‌های فارسی در متن پیام‌ها."""
import collections
import re
from pathlib import Path

path = Path(__file__).resolve().parent.parent / "data" / "practice_chat.txt"
raw = path.read_text(encoding="utf-8")

HEADER = re.compile(
    r"^(.+?),\s*\[(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2})\]\s*$"
)
WORD = re.compile(r"[\u0600-\u06FF]{2,}")
SKIP_BODY = {"❤", "👍", "In reply to this message"}

STOP = set(
    """از در به با که این آن را هم می من تو ما شما او برای اگر یا نه تا هر چه
    است هست شد شده رو روی یک یه و اما ولی چون پس یعنی دیگه فقط بود بودم بوده
    باشه باشم کنی کنم کنید هستم هستی دارم داری داره داریم خود خودم خیلی خوب
    خوبی ها بچه همگی همین بعد قبل چیز چی کی اینکه اون الان منم """.split()
)


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
        messages.append({"text": body})
    cur = None


for line in raw.splitlines():
    m = HEADER.match(line)
    if m:
        flush()
        cur = {"body_lines": []}
        continue
    if cur is None or line.strip() == "":
        continue
    cur["body_lines"].append(line)
flush()

bag = collections.Counter()
for msg in messages:
    text = msg["text"]
    if text.startswith("Voice message"):
        continue
    for w in WORD.findall(text):
        if w not in STOP:
            bag[w] += 1

print("unique words:", len(bag))
for w, n in bag.most_common(15):
    print(f"{n:3d}  {w}")
