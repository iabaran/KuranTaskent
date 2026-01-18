# -*- coding: utf-8 -*-
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Load data
with open('quran_arabic.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Toplam sure sayısı: {len(data)}")

# Test first surah
first_surah = data[0]
print(f"\nİlk sure: {first_surah['name']} (ID: {first_surah['id']})")
print(f"İlk ayet: {first_surah['verses'][0]['text']}")
print(f"3. ayet: {first_surah['verses'][2]['text']}")

# Count Rahman occurrences
basmala_rahman = 0
other_rahman = 0
all_rahman_locations = []

for surah in data:
    surah_num = surah['id']
    
    for verse in surah['verses']:
        verse_num = verse['id']
        text = verse['text']
        
        # Check if text contains Rahman (check multiple variations)
        has_rahman = ('رحمن' in text or 'رَحۡمَٰن' in text or 'رَّحۡمَٰن' in text or 
                     'الرحمن' in text or 'ٱلرَّحۡمَٰن' in text)
        
        if has_rahman:
            all_rahman_locations.append((surah_num, verse_num, text[:50]))
            
            # Is this a Basmala? (verse 1, not Surah 9, contains both Rahman and Rahim)
            is_basmala = (verse_num == 1 and surah_num != 9 and 
                         ('رحيم' in text or 'رَّحِيم' in text))
            
            if is_basmala:
                basmala_rahman += 1
            else:
                other_rahman += 1

print(f"\n{'='*60}")
print(f"📊 RAHMAN ANALİZİ")
print(f"{'='*60}")
print(f"Besmelelerdeki Rahman: {basmala_rahman}")
print(f"Diğer ayetlerdeki Rahman: {other_rahman}")
print(f"TOPLAM: {basmala_rahman + other_rahman}")
print(f"{'='*60}")

print(f"\nİlk 15 Rahman geçişi:")
for i, (s, v, txt) in enumerate(all_rahman_locations[:15], 1):
    print(f"{i:2d}. {s:3d}:{v:3d} - {txt}...")
