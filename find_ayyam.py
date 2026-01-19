#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Kur'an'da أيام (günler - çoğul) kelimesini arar
"""

import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('quran_arabic.json', 'r', encoding='utf-8') as f:
    quran = json.load(f)

def normalize(t):
    return re.sub(r'[\u064B-\u065F\u0670\u06D6-\u06ED\u0640\u0653-\u0655]', '', t)

# أيام and variants - we search for the core letters
# ا ي ا م or أ ي ا م
ayyam_core = 'يام'  # Core without hamza

count = 0
found_words = {}

for s in quran:
    for v in s.get('verses', []):
        for w in v['text'].split():
            nw = normalize(w)
            if ayyam_core in nw and 'يوم' not in nw:  # Contains يام but not يوم
                count += 1
                if w not in found_words:
                    found_words[w] = []
                found_words[w].append(f"{s['id']}:{v['id']}")
                print(f"{s['id']}:{v['id']} - {w}")

print(f"\nBulunan formlar:")
for word, verses in sorted(found_words.items(), key=lambda x: -len(x[1])):
    print(f"  {word}: {len(verses)} kez")

print(f"\nToplam ÇOĞUL (أيام): {count}")
