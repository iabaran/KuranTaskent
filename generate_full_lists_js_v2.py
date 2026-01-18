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
basmalas = []
basmalas.append({'s': 1, 'a': 1}) # Fatiha

for s in range(2, 115):
    if s == 9: continue 
    basmalas.append({'s': s, 'h': 1})

# Explicitly add 27:30 
basmalas.append({'s': 27, 'a': 30})

basmalas.sort(key=lambda x: (x['s'], x.get('a', 0)))

# Rahman Data
final_rahman = []
# Add all Basmalas
for b in basmalas:
    item = b.copy()
    item['is_basmala'] = True
    final_rahman.append(item)

# Add textual occurrences avoiding Basmala duplicates
for loc in rahman_locs:
    # Check if this matches a BASMALA
    is_basmala_match = False
    for b in basmalas:
        if b['s'] == loc['s'] and b.get('a') == loc['a']:
            is_basmala_match = True
            break
    
    if not is_basmala_match:
        final_rahman.append(loc)

# Sort
def sort_key(x):
    a = x.get('a', 0)
    return (x['s'], a)

final_rahman.sort(key=sort_key)

# Rahim Data
final_rahim = []
for b in basmalas:
    item = b.copy()
    item['is_basmala'] = True
    final_rahim.append(item)

for loc in rahim_locs:
    is_basmala_match = False
    for b in basmalas:
        if b['s'] == loc['s'] and b.get('a') == loc['a']:
            is_basmala_match = True
            break
    
    if not is_basmala_match:
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
