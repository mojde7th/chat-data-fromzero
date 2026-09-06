# -*- coding: utf-8 -*-
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
"""07 — ساخت dashboard.html با Chart.js از روی همان دادهٔ تمرین."""
import collections
import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
path = BASE / "data" / "practice_chat.txt"
out = Path(__file__).resolve().parent / "dashboard.html"
# اگر از my-lab اجرا شود، خروجی کنار اسکریپت کاربر می‌ماند
if Path(__file__).resolve().parent.name == "my-lab":
    out = Path(__file__).resolve().parent / "dashboard.html"
else:
    out = BASE / "solutions" / "dashboard.html"

raw = path.read_text(encoding="utf-8")
HEADER = re.compile(
    r"^(.+?),\s*\[(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2})\]\s*$"
)
WORD = re.compile(r"[\u0600-\u06FF]{2,}")
DUR = re.compile(r"^(\d{2}):(\d{2}),\s*[\d.]+\s*KB\s*$", re.I)
SKIP_BODY = {"❤", "👍", "In reply to this message"}
STOP = set(
    """از در به با که این آن را هم می من تو ما شما او برای اگر یا نه تا هر چه
    است هست شد شده رو روی یک یه و اما ولی چون پس یعنی دیگه فقط بود بودم بوده
    باشه باشم کنی کنم کنید هستم هستی دارم داری داره داریم خود خودم خیلی خوب
    خوبی ها بچه همگی همین بعد قبل چیز چی کی اینکه اون الان منم """.split()
)
CATEGORIES = {
    "خواب": ["خواب", "بیدار"],
    "ورزش": ["ورزش", "پیاده‌روی", "پیاده"],
    "تمرکز": ["تمرکز", "تعلل", "تایمر", "اعلان"],
    "عادت": ["عادت", "عادت‌های", "عادت‌ها"],
    "ترس": ["ترس", "شکست", "ارائه"],
    "مطالعه": ["مطالعه", "کتاب", "خواندم", "صفحه", "خلاصه"],
}


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
voices = []
cur = None
expect_dur = False


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
        who = canon(m.group(1))
        cur = {"who": who, "body_lines": []}
        expect_dur = False
        continue
    if line.strip() == "Voice message":
        expect_dur = True
        if cur is not None:
            cur["body_lines"].append(line)
        continue
    if expect_dur:
        d = DUR.match(line.strip())
        if d and cur is not None:
            secs = int(d.group(1)) * 60 + int(d.group(2))
            voices.append({"who": cur["who"], "seconds": secs})
        expect_dur = False
    if cur is None or line.strip() == "":
        continue
    if line.strip() != "Voice message":
        cur["body_lines"].append(line)
flush()

people = collections.Counter(m["who"] for m in messages)
bag = collections.Counter()
for m in messages:
    if m["text"].startswith("Voice message"):
        continue
    for w in WORD.findall(m["text"]):
        if w not in STOP:
            bag[w] += 1
cats = collections.Counter()
for m in messages:
    text = m["text"]
    hit = False
    for cat, keys in CATEGORIES.items():
        if any(k in text for k in keys):
            cats[cat] += 1
            hit = True
    if not hit:
        cats["سایر"] += 1

people_l = [w for w, _ in people.most_common()]
people_v = [people[w] for w in people_l]
words_l = [w for w, _ in bag.most_common(12)]
words_v = [bag[w] for w in words_l]
cats_l = list(cats.keys())
cats_v = [cats[c] for c in cats_l]
voice_by = collections.Counter()
for v in voices:
    voice_by[v["who"]] += v["seconds"]
voice_l = [w for w, _ in voice_by.most_common()]
voice_v = [voice_by[w] for w in voice_l]

payload = {
    "people_labels": people_l,
    "people_values": people_v,
    "words_labels": words_l,
    "words_values": words_v,
    "cats_labels": cats_l,
    "cats_values": cats_v,
    "voice_labels": voice_l,
    "voice_values": voice_v,
    "msg_count": len(messages),
    "voice_count": len(voices),
}

html = f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Chat Data Dashboard</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
body{{margin:0;font-family:Tahoma,sans-serif;background:#0b1016;color:#e8eef5}}
main{{max-width:960px;margin:0 auto;padding:20px}}
h1{{font-size:1.2rem}}
.grid{{display:grid;gap:16px;grid-template-columns:1fr}}
@media(min-width:800px){{.grid{{grid-template-columns:1fr 1fr}}}}
.card{{background:#121a22;border:1px solid #2a3542;border-radius:12px;padding:12px}}
canvas{{max-height:280px}}
.meta{{color:#8fa3b8;font-size:.9rem}}
</style>
</head>
<body>
<main>
  <h1>داشبورد دادهٔ چت تمرین</h1>
  <p class="meta">پیام‌ها: {payload['msg_count']} — ویس‌ها: {payload['voice_count']}</p>
  <div class="grid">
    <div class="card"><canvas id="cPeople"></canvas></div>
    <div class="card"><canvas id="cWords"></canvas></div>
    <div class="card"><canvas id="cCats"></canvas></div>
    <div class="card"><canvas id="cVoice"></canvas></div>
  </div>
</main>
<script>
const D = {json.dumps(payload, ensure_ascii=False)};
const mk = (id, type, labels, values, label) => new Chart(document.getElementById(id), {{
  type,
  data: {{ labels, datasets: [{{ label, data: values, backgroundColor: ['#7ec8ce','#7dcea0','#e2b657','#e07a7a','#cbb6f0','#6db3f2','#f0b429','#3ecf8e'] }}] }},
  options: {{ plugins: {{ legend: {{ display: type === 'pie' }} }}, scales: type === 'pie' ? {{}} : {{ y: {{ beginAtZero: true }} }} }}
}});
mk('cPeople', 'bar', D.people_labels, D.people_values, 'پیام');
mk('cWords', 'bar', D.words_labels, D.words_values, 'واژه');
mk('cCats', 'pie', D.cats_labels, D.cats_values, 'دسته');
mk('cVoice', 'bar', D.voice_labels, D.voice_values, 'ثانیه ویس');
</script>
</body>
</html>
"""

out.write_text(html, encoding="utf-8")
print("wrote:", out)
