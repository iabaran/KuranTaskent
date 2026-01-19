#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
أيام (günler) kelimesinin geçtiği 26 ayeti Türkçe mealleriyle listeler
"""

import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('quran_arabic.json', 'r', encoding='utf-8') as f:
    quran = json.load(f)

# Türkçe meal yükle
with open('quran_tr_js.js', 'r', encoding='utf-8') as f:
    tr_content = f.read()

tr_data = {}
matches = re.findall(r'\[(\d+),(\d+),"([^"]*)"\]', tr_content)
for m in matches:
    key = f"{m[0]}:{m[1]}"
    tr_data[key] = m[2]

def norm(t):
    return re.sub(r'[\u064B-\u065F\u0670\u06D6-\u06ED\u0640\u0653-\u0655]', '', t)

print("GÜNLER (أيام) - TÜM GEÇİŞLER")
print("=" * 70)

count = 0
results = []

for s in quran:
    for v in s.get('verses', []):
        for w in v['text'].split():
            nw = norm(w)
            if 'ايام' in nw or 'أيام' in nw:
                count += 1
                key = f"{s['id']}:{v['id']}"
                tr = tr_data.get(key, 'Meal bulunamadı')
                results.append({
                    'ref': key,
                    'word': w,
                    'tr': tr
                })

for r in results:
    print(f"\n{results.index(r)+1}. {r['ref']} - {r['word']}")
    print(f"   {r['tr'][:100]}...")

print(f"\n{'='*70}")
print(f"TOPLAM: {count}")
