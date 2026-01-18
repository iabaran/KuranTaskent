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

# Invalid word forms that look like Allah/Lillah but meanings are different
INVALID_FORMS = [
    'خللها', 'خلله', 'يضلله', 'وظللهم', 'ظلله', 
    'خللهما', 'ٱللهو', 'ظللها', 'ٱللهب', 'للهدى'
]

print("--- DETAILED ALLAH ANALYSIS ---")

list_standard = []
list_allahumma = []
list_headers = []

# 1. VERSES
for surah in data:
    for verse in surah['verses']:
        clean_text = remove_diacritics(verse['text'])
        words = clean_text.split()
        
        for w in words:
            w_clean = re.sub(r'[^\w\s]', '', w)
            
            if 'الله' in w_clean or 'لله' in w_clean:
                # 1. Filter Invalid Meanings
                if w_clean in INVALID_FORMS:
                    continue
                
                # 2. Check for Allahumma (اللهم)
                if 'اللهم' in w_clean:
                    list_allahumma.append({'s': surah['id'], 'a': verse['id']})
                else:
                    # Standard Allah (inc. Billah, Lillah, Tallahi...)
                    list_standard.append({'s': surah['id'], 'a': verse['id']})

# 2. HEADERS (Unnumbered Basmalas)
# Surahs 2-114 (exc 9) have headers.
for s in range(1, 115):
    if s == 1: continue # Fatiha 1 is verse
    if s == 9: continue # Tawbah has no basmala
    list_headers.append({'s': s, 'h': 1})

# RESULTS
cnt_std = len(list_standard)
cnt_all = len(list_allahumma)
cnt_head = len(list_headers)

print(f"Standard Allah in Verses: {cnt_std}")
print(f"Allahumma in Verses: {cnt_all}")
print(f"Allah in Headers (Basmalas): {cnt_head}")
print("-" * 20)
print(f"TOTAL (Verses Standard): {cnt_std}")
print(f"TOTAL (Verses All): {cnt_std + cnt_all}")
print(f"TOTAL (Verses + Headers): {cnt_std + cnt_all + cnt_head}")

# Check specific verse Tevbe 129
has_tevbe_129 = any(x['s'] == 9 and x['a'] == 129 for x in list_standard)
print(f"Includes Tevbe 129: {has_tevbe_129}")

# Generate JS Code
print("\nJS Arrays:")
print("const allahData = [")
# We will combine all lists? Or user wants total?
# Let's provide the Standard List + Headers (marked h:1) + Allahumma?
# Usually tooltips just show "Allah". So list ALL valid occurrences.
# We will omit Allahumma if it's strictly not "Allah". Allahumma = "O Allah".
# User asked "Allah". Allahumma contains "Allah".
# I will include EVERYTHING but maybe mark types.
# Or better: Standard + Headers. 
# 2699 + 112 = 2811.

# Creating combined sorted list
full_list = []
# Add headers
for h in list_headers:
    full_list.append(h)
    
# Add verses (Standard)
for v in list_standard:
    full_list.append(v)

# Add allahumma?
for v in list_allahumma:
    # v['type'] = 'allahumma' # JS doesn't handle type yet, simplified locs
    full_list.append(v)

# Sort by Surah, Verse (Header h:1 is conceptually "before" verse 1, usually)
# My sort logic in JS handles headers?
# In python:
full_list.sort(key=lambda x: (x['s'], x.get('a', 0))) 

entries = []
for x in full_list:
    if 'h' in x:
        entries.append(f"{{s:{x['s']}, h:1}}")
    else:
        entries.append(f"{{s:{x['s']}, a:{x['a']}}}")

print(", ".join(entries))
print("];")
