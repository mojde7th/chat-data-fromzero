# -*- coding: utf-8 -*-
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
"""06 — جمع مدت ویس‌ها از خط‌های Voice message."""
import re
from pathlib import Path

path = Path(__file__).resolve().parent.parent / "data" / "practice_chat.txt"
raw = path.read_text(encoding="utf-8")

HEADER = re.compile(
    r"^(.+?),\s*\[(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2})\]\s*$"
)
DUR = re.compile(r"^(\d{2}):(\d{2}),\s*[\d.]+\s*KB\s*$", re.I)


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


voices = []
cur_who = None
expect_dur = False

for line in raw.splitlines():
    m = HEADER.match(line)
    if m:
        cur_who = canon(m.group(1))
        expect_dur = False
        continue
    if line.strip() == "Voice message":
        expect_dur = True
        continue
    if expect_dur:
        d = DUR.match(line.strip())
        if d:
            secs = int(d.group(1)) * 60 + int(d.group(2))
            voices.append({"who": cur_who, "seconds": secs, "raw": line.strip()})
        expect_dur = False

total = sum(v["seconds"] for v in voices)
print("voice count:", len(voices))
print("total seconds:", total)
print("total mm:ss:", f"{total // 60:02d}:{total % 60:02d}")
for v in voices:
    print(f"{v['who']:6s}  {v['seconds']:4d}s  {v['raw']}")
