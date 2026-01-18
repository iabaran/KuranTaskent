# -*- coding: utf-8 -*-
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Load data
with open('quran_arabic.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Rahman variations to search for
rahman_variations = [
    'الرحمن',  # Al-Rahman (most common)
    'رحمن',    # Rahman without Al
]

# Normalize function to remove diacritics
import re
normalize = lambda t: re.sub(r'[\u064B-\u065F\u0670]', '', t)

# Count Rahman in Basmalas (first verse of each surah except Surah 9)
basmala_rahman_count = 0
basmala_locations = []

for surah in data:
    surah_num = surah['id']
    # Skip Surah 9 (Tawbah) - it doesn't have Basmala
    if surah_num == 9:
        continue
    
    # Check first verse
    if surah['verses'] and len(surah['verses']) > 0:
        first_verse = surah['verses'][0]
        if first_verse['id'] == 1:
            normalized_text = normalize(first_verse['text'])
            # Check if this is a Basmala (contains both Rahman and Rahim)
            if 'الرحمن' in normalized_text and 'الرحيم' in normalized_text:
                basmala_rahman_count += 1
                basmala_locations.append(f"{surah_num}:1")

print(f"Besmelelerdeki Rahman sayısı: {basmala_rahman_count}")
print(f"\nBesmele olan sureler (ilk 10):")
for loc in basmala_locations[:10]:
    print(f"  {loc}")

# Now count all other Rahman occurrences (non-Basmala)
other_rahman_count = 0
other_locations = []

for surah in data:
    for verse in surah['verses']:
        normalized_text = normalize(verse['text'])
        
        # Check if Rahman exists
        if 'الرحمن' in normalized_text:
            # Check if this is NOT a Basmala
            # Basmala pattern: contains both الرحمن and الرحيم
            is_basmala = ('الرحمن' in normalized_text and 
                         'الرحيم' in normalized_text and 
                         verse['id'] == 1 and 
                         surah['id'] != 9)
            
            if not is_basmala:
                other_rahman_count += 1
                other_locations.append(f"{surah['id']}:{verse['id']}")

print(f"\nBesmele dışındaki Rahman sayısı: {other_rahman_count}")
print(f"\nBesmele dışındaki Rahman'lar (ilk 10):")
for loc in other_locations[:10]:
    print(f"  {loc}")

print(f"\n{'='*50}")
print(f"TOPLAM Rahman (Besmele + Diğer): {basmala_rahman_count + other_rahman_count}")
print(f"  - Besmelelerde: {basmala_rahman_count}")
print(f"  - Diğer ayetlerde: {other_rahman_count}")
print(f"{'='*50}")
