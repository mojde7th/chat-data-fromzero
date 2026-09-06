# -*- coding: utf-8 -*-
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
"""01 — فقط خواندن فایل تمرین و چاپ چند خط اول."""
from pathlib import Path

# مسیر نسبی از پوشه my-lab: یک سطح بالاتر، بعد data
path = Path(__file__).resolve().parent.parent / "data" / "practice_chat.txt"

text = path.read_text(encoding="utf-8")
lines = text.splitlines()

print("path:", path)
print("chars:", len(text))
print("lines:", len(lines))
print("--- first 12 lines ---")
for i, line in enumerate(lines[:12], start=1):
    print(f"{i:02d}| {line}")
