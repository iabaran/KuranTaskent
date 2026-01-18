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

print("--- SEARCHING FOR JANNAH VARIANTS ---")

found_words = {}

for surah in data:
    for verse in surah['verses']:
        clean = remove_diacritics(verse['text'])
        words = clean.split()
        for w in words:
            # Check if root chars j-n-n are present in order
            # This is a loose heuristic
            if 'ج' in w and 'n' not in w: # Python strings don't work like this easily for arabic chars ordering without regex
                pass
            
            # Search for anything starting with J-N
            if w.startswith('جن') or w.startswith('و جن') or w.startswith('ٱلجن') or 'جنة' in w:
                 if w not in found_words:
                     found_words[w] = 0
                 found_words[w] += 1

print("\nPotential Jannah Forms Found:")
for w, c in sorted(found_words.items(), key=lambda x: x[1], reverse=True):
    print(f"{w}: {c}")
