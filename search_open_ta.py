# -*- coding: utf-8 -*-
import json
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('quran_arabic.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def remove_diacritics(text):
    text = re.sub(r'[\u064B-\u065F\u0670\u0617-\u061A\u06D6-\u06ED]', '', text)
    return text

print("--- SEARCHING FOR OPEN TA (جنت) VARIANTS ---")

matches = []

for surah in data:
    for verse in surah['verses']:
        clean = remove_diacritics(verse['text'])
        words = clean.split()
        for w in words:
            w_clean = re.sub(r'[^\w\s]', '', w)
            # Find words ending with 'j-n-t' (open ta)
            # But clearly related to Jannah
            if w_clean.endswith('جنت') and 'جنت' in w_clean:
                # Exclude obvious plurals if we can distinguish?
                # Usually 'Jannat' is plural.
                # But sometimes Singular Jannah is written as Jannat.
                matches.append(f"{surah['id']}:{verse['id']} - {w_clean}")

print(f"Total Matches: {len(matches)}")
for m in matches:
    print(m)
