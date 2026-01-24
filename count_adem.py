#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Kur'an'da Adem (آدم) kelimesini sayan script
"""

import json
import re

# Quran Arabic JSON dosyasını yükle
with open('quran_arabic.json', 'r', encoding='utf-8') as f:
    quran = json.load(f)

# Adem kelimesi - Arapça yazılışı
adem_patterns = [
    'آدَمَ',      # Adem (mansub/accusative)
    'آدَمُ',      # Adem (marfu/nominative) 
    'آدَمِ',      # Adem (mecrur/genitive)
    'آدَم',       # Adem (genel)
    'ءَادَمَ',    # Alternatif yazılış
    'ءَادَم',     # Alternatif yazılış
]

# Harekesiz normalize etme fonksiyonu
def normalize_arabic(text):
    """Harekeler ve uzatma işaretlerini kaldır"""
    # Harekeler: fatha, damma, kasra, sukun, shadda, tanwin vb.
    diacritics = re.compile(r'[\u064B-\u065F\u0670\u06D6-\u06ED\u0640\u0653-\u0655]')
    return diacritics.sub('', text)

# Basit pattern: آدم - harekesiz
adem_base = 'آدم'
# Alternatif yazılış: ءادم (hemze ile)
adem_alt = 'ءادم'

results = []
total_count = 0

for surah in quran:
    surah_num = surah['id']
    surah_name = surah.get('name', f'Sure {surah_num}')
    
    for verse in surah['verses']:
        verse_num = verse['id']
        text = verse['text']
        normalized_text = normalize_arabic(text)
        
        # Adem kelimesini ara (harekesiz)
        count = normalized_text.count(adem_base) + normalized_text.count(adem_alt)
        
        if count > 0:
            total_count += count
            results.append({
                'surah': surah_num,
                'surah_name': surah_name,
                'verse': verse_num,
                'count': count,
                'text': text
            })

print("=" * 80)
print("ADEM (آدم) KELİMESİ - KUR'AN ANALİZİ")
print("=" * 80)
print(f"\nToplam geçiş sayısı: {total_count}\n")
print("-" * 80)

for i, r in enumerate(results, 1):
    print(f"{i}. {r['surah_name']} ({r['surah']}:{r['verse']})")
    print(f"   {r['text'][:100]}..." if len(r['text']) > 100 else f"   {r['text']}")
    print()

print("-" * 80)
print(f"\n📊 ÖZET: Adem (آدم) kelimesi Kur'an'da toplam {total_count} kere geçmektedir.")
print(f"📍 {len(results)} farklı ayette bulunmaktadır.")

# JavaScript data formatında çıktı
print("\n\n// JavaScript Data Format:")
print("const ademData = [")
for r in results:
    print(f"    {{ s: {r['surah']}, a: {r['verse']} }},")
print("];")
