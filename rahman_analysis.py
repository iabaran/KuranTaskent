# -*- coding: utf-8 -*-
"""
Kur'an'da "Rahman" kelimesinin geçtiği yerleri analiz eden script.
"""

import json
import re
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def normalize_arabic(text):
    """Arapça metni normalize et (harekeleri kaldır)"""
    if not text:
        return ""
    # Hareke ve diğer işaretleri kaldır
    text = re.sub(r'[\u064B-\u065F\u0670]', '', text)
    return text.strip()

# Load JSON
with open('quran_arabic.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=" * 80)
print("RAHMAN KELİMESİNİN DETAYLI KONTROLÜ")
print("=" * 80)

# Rahman kelimesini ara (Dagger Alif ile: رحمٰن)
# Not: Dagger Alif (ٰ) Unicode: U+0670
rahman_patterns = [
    'رحمن',   # Harekesiz (normal)
    'رحمٰن',  # Dagger Alif ile
]
total_count = 0
occurrences = []

for surah in data:
    surah_id = surah['id']
    surah_name = surah['transliteration']
    
    for verse in surah['verses']:
        verse_id = verse['id']
        text = verse['text']
        normalized = normalize_arabic(text)
        
        # Check both patterns
        count = 0
        for pattern in rahman_patterns:
            count += text.count(pattern)  # Use original text, not normalized
        
        if count > 0:
            total_count += count
            for i in range(count):
                occurrences.append({
                    'surah': surah_id,
                    'surah_name': surah_name,
                    'verse': verse_id,
                    'text': text
                })
                print(f"Sure {surah_id:3d} ({surah_name}), Ayet {verse_id:3d}")

print("\n" + "=" * 80)
print("ÖZET:")
print("=" * 80)
print(f"TOPLAM Rahman: {total_count}")
print("=" * 80)

# JavaScript array formatında çıktı
print("\n" + "=" * 80)
print("JAVASCRIPT ARRAY (KuranOkuyucu.html için):")
print("=" * 80)
print("const rahmanData = [")
for i, occ in enumerate(occurrences):
    comma = "," if i < len(occurrences) - 1 else ""
    print(f"    {{ s: {occ['surah']}, a: {occ['verse']} }}{comma}")
print("];")
print(f"\n// Toplam: {total_count} Rahman")
