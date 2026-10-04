"""Build the AG News "news feed" document used in the lab.

Input:  ag_news_test.csv (original AG News test split: label, title, description;
        labels 1=World, 2=Sports, 3=Business, 4=Sci/Tech)
Output: agnews_feed.json          [{"content": "<N articles concatenated>"}]
        agnews_ground_truth.txt   true number of articles per category

Usage:  python prepare_agnews.py
"""

import csv
import json
import random
import re
from pathlib import Path

HERE = Path(__file__).parent
SEED = 0
# Deliberately unbalanced, so "about the same per category" is visibly wrong.
MIX = {"World": 160, "Sports": 120, "Business": 80, "Sci/Tech": 40}
LABELS = {"1": "World", "2": "Sports", "3": "Business", "4": "Sci/Tech"}


def clean(text: str) -> str:
    text = re.sub(r"#(\d+);", lambda m: chr(int(m.group(1))), text)  # "#36;" -> "$"
    text = text.replace("\\", " ")  # AG News uses backslashes as line breaks
    return re.sub(r"\s+", " ", text).strip()


with open(HERE / "ag_news_test.csv", newline="", encoding="utf-8") as f:
    rows = [(LABELS[label], clean(title), clean(desc)) for label, title, desc in csv.reader(f)]

rng = random.Random(SEED)
picked = []
for category, n in MIX.items():
    picked += rng.sample([r for r in rows if r[0] == category], n)
rng.shuffle(picked)

articles = [f"[A{i:03d}] {title}. {desc}" for i, (_, title, desc) in enumerate(picked, 1)]
(HERE / "agnews_feed.json").write_text(json.dumps([{"content": "\n\n".join(articles)}], indent=1))

total = sum(MIX.values())
lines = [f"AG News feed: {total} articles (seed={SEED})", ""]
lines += [f"{category}: {n}" for category, n in MIX.items()]
lines += ["", "Article id -> category:"]
lines += [f"A{i:03d}\t{category}" for i, (category, _, _) in enumerate(picked, 1)]
(HERE / "agnews_ground_truth.txt").write_text("\n".join(lines) + "\n")

print(f"wrote {total} articles to agnews_feed.json and agnews_ground_truth.txt")
