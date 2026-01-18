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

print("--- ALLAH FORM ANALYSIS ---")

forms = {}

for surah in data:
    for verse in surah['verses']:
        clean_text = remove_diacritics(verse['text'])
        words = clean_text.split()
        
        for w in words:
            w_clean = re.sub(r'[^\w\s]', '', w)
            
            # Use same logic as before to capture candidates
            if 'الله' in w_clean or 'لله' in w_clean:
                if w_clean not in forms:
                    forms[w_clean] = 0
                forms[w_clean] += 1

print("\nWord Forms Found:")
sorted_forms = sorted(forms.items(), key=lambda x: x[1], reverse=True)
for w, c in sorted_forms:
    print(f"{w}: {c}")

print(f"\nTotal Word Types: {len(forms)}")
