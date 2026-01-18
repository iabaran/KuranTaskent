# -*- coding: utf-8 -*-
import json
import sys
import re
sys.stdout.reconfigure(encoding='utf-8')

# Load data
with open('quran_arabic.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Normalize function to remove diacritics
normalize = lambda t: re.sub(r'[\u064B-\u065F\u0670]', '', t)

# Count Rahman in Basmalas
basmala_count = 0
basmala_surahs = []

# Count other Rahman occurrences
other_rahman = []

for surah in data:
    surah_num = surah['id']
    
    for verse in surah['verses']:
        verse_num = verse['id']
        text = verse['text']
        normalized = normalize(text)
        
        # Check if Rahman exists
        if 'الرحمن' in normalized:
            # Is this verse 1 and not Surah 9?
            if verse_num == 1 and surah_num != 9:
                # This is likely a Basmala
                basmala_count += 1
                basmala_surahs.append(surah_num)
            else:
                # This is a non-Basmala Rahman
                other_rahman.append((surah_num, verse_num))

print(f"📊 RAHMAN KELİMESİ ANALİZİ")
print(f"{'='*60}")
print(f"\n✅ Besmelelerdeki Rahman: {basmala_count} adet")
print(f"   (Tevbe suresi hariç, her surenin başındaki Besmele)")
print(f"\n✅ Diğer ayetlerdeki Rahman: {len(other_rahman)} adet")
print(f"\n{'='*60}")
print(f"🎯 TOPLAM RAHMAN: {basmala_count + len(other_rahman)} adet")
print(f"{'='*60}")

print(f"\n📝 Detay:")
print(f"   - Besmelelerde: {basmala_count}")
print(f"   - Besmele dışında: {len(other_rahman)}")

# Show first 10 non-Basmala occurrences
if other_rahman:
    print(f"\n📖 Besmele dışındaki ilk 10 Rahman:")
    for s, v in other_rahman[:10]:
        print(f"   {s}:{v}")
