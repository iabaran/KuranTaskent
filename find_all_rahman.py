# -*- coding: utf-8 -*-
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Load data
with open('quran_arabic.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Search for all variations of Rahman
rahman_variations = [
    'ٱلرَّحۡمَٰنِ',  # With Al prefix and diacritics
    'ٱلرَّحۡمَٰن',   # Variation
    'رَّحۡمَٰنِ',    # Without Al
    'رَّحۡمَٰن',     # Variation
    'ٱلرَّحْمَٰنِ',  # Different diacritic
    'ٱلرَّحْمَٰن',   # Variation
]

results = []
for surah in data:
    for verse in surah['verses']:
        text = verse['text']
        # Check if any variation exists
        for var in rahman_variations:
            if var in text:
                results.append({
                    's': surah['id'],
                    'a': verse['id'],
                    'text': text
                })
                print(f"{surah['id']:3d}:{verse['id']:3d} - Found: {var}")
                break

print(f"\n\nToplam: {len(results)} Rahman bulundu")

# Also search with normalized (no diacritics)
print("\n\nNormalize edilmiş arama:")
import re
normalize = lambda t: re.sub(r'[\u064B-\u065F\u0670]', '', t)

rahman_normalized = 'الرحمن'
count2 = 0
for surah in data:
    for verse in surah['verses']:
        if rahman_normalized in normalize(verse['text']):
            count2 += 1
            if count2 <= 10:
                print(f"{surah['id']:3d}:{verse['id']:3d}")

print(f"\nNormalize ile toplam: {count2}")
