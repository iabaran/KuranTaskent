# -*- coding: utf-8 -*-
import json
import sys
import re

# Load data
with open('quran_arabic.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def remove_diacritics(text):
    arabic_diacritics = re.compile(r'[\u064B-\u065F\u0670\u0617-\u061A\u06D6-\u06ED]')
    return arabic_diacritics.sub('', text)

def get_occurrences(word):
    locs = []
    for surah in data:
        for verse in surah['verses']:
            clean = remove_diacritics(verse['text'])
            if word in clean:
                count = clean.count(word)
                for _ in range(count):
                    locs.append({'s': surah['id'], 'a': verse['id']})
    return locs

rahman_locs = get_occurrences('رحمن')
rahim_locs = get_occurrences('رحيم')

# Define Basmalas (114)
# 1. Fatiha 1:1
# 2. Neml 27:30
# 3. Headers of Surahs 2-8, 10-27, 28-114
basmalas = []
basmalas.append({'s': 1, 'a': 1}) # Fatiha

# Add headers
for s in range(2, 115):
    if s == 9: continue # Tawbah has no Basmala
    if s == 27:
        # Surah 27 has header AND 27:30
        basmalas.append({'s': 27, 'h': 1}) # Header
        # We also need to add 27:30 to Basmalas list?
        # User considers 27:30 as the "missing" Basmala.
        # But wait, 27 has a header too? Yes.
        # So 27 has TWO Basmalas? 
        # Standard count: 113 Headers + 1 (27:30) = 114.
        # But Surah 1 doesn't have a "Header" separate from 1:1?
        # Usually 1:1 IS the Basmala.
        # So:
        # 1:1 (1)
        # Headers of 2-9[X]... (112 headers)
        # 27:30 (1)
        # Total 114.
        pass
    
    # Add regular header
    # Note: For s=27, we add header here too
    basmalas.append({'s': s, 'h': 1})

# Explicitly add 27:30 to Basmalas if not covered
# (The loop above added 27 Header. 27:30 is separate)
basmalas.append({'s': 27, 'a': 30})

# Sort Basmalas
basmalas.sort(key=lambda x: (x['s'], x.get('a', 0)))

# Rahman Data
# Start with Basmalas
rahman_data = []
# We need to distinguish "Header" vs "Verse" in the final list for the Tooltip
# BUT we also need to avoid duplicates with the "Textual" search.

# Textual occurrences of Rahman
text_rahman = rahman_locs

# We want to put ALL Basmalas in the list.
# For 1:1 and 27:30, they are in text_rahman.
# We should use the "Basmala" version (maybe with a flag) and REMOVE from text_rahman.

# Create final list
final_rahman = []

# Add all 114 Basmalas
for b in basmalas:
    # Check if this basmala is in textual list
    # 1:1 and 27:30 should be there. Headers are not.
    item = b.copy()
    item['is_basmala'] = True
    final_rahman.append(item)

# Add remaining textual occurrences
for loc in text_rahman:
    # Check if this loc is already in final_rahman (e.g. 1:1 or 27:30)
    is_present = False
    for b in final_rahman:
        if b['s'] == loc['s'] and b.get('a') == loc['a']:
            is_present = True
            break
    
    if not is_present:
        final_rahman.append(loc)

# Sort final list
def sort_key(x):
    # s then a (header a is treated as 0 for sort)
    a = x.get('a', 0)
    return (x['s'], a)

final_rahman.sort(key=sort_key)

# Rahim Data (Same logic)
text_rahim = rahim_locs
final_rahim = []

for b in basmalas:
    item = b.copy()
    item['is_basmala'] = True
    final_rahim.append(item)

for loc in text_rahim:
    is_present = False
    for b in final_rahim:
        if b['s'] == loc['s'] and b.get('a') == loc['a']:
            is_present = True
            break
    
    if not is_present:
        final_rahim.append(loc)

final_rahim.sort(key=sort_key)

print(f"Rahman Count: {len(final_rahman)}")
print(f"Rahim Count: {len(final_rahim)}")

# Generate JS strings
print("\nRAHMAN_JS_START")
print("const rahmanData = [")
lines = []
for item in final_rahman:
    if 'h' in item:
        lines.append(f"{{s:{item['s']}, h:1}}")
    else:
        lines.append(f"{{s:{item['s']}, a:{item['a']}}}")
# Chunk for display
print(", ".join(lines))
print("];")
print("RAHMAN_JS_END")

print("\nRAHIM_JS_START")
print("const rahimData = [")
lines = []
for item in final_rahim:
    if 'h' in item:
        lines.append(f"{{s:{item['s']}, h:1}}")
    else:
        lines.append(f"{{s:{item['s']}, a:{item['a']}}}")
print(", ".join(lines))
print("];")
print("RAHIM_JS_END")
