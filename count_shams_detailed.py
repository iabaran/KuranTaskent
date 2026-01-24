#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Kur'an'da Güneş (شمس) kelimesini detaylı inceleyen script
"""

import json
import re

# Quran Arabic JSON dosyasını yükle
with open('quran_arabic.json', 'r', encoding='utf-8') as f:
    quran = json.load(f)

def normalize_arabic(text):
    """Harekeler ve uzatma işaretlerini kaldır"""
    diacritics = re.compile(r'[\u064B-\u065F\u0670\u06D6-\u06ED\u0640\u0653-\u0655]')
    return diacritics.sub('', text)

target_root = 'شمس'
matches = []

print("=" * 80)
print("GÜNEŞ (شمس) KELİMESİ DETAYLI ANALİZİ")
print("=" * 80)

for surah in quran:
    surah_num = surah['id']
    for verse in surah['verses']:
        verse_num = verse['id']
        text = verse['text']
        normalized_text = normalize_arabic(text)
        
        words = text.split()
        for i, word in enumerate(words):
            clean_word = normalize_arabic(word)
            
            # İçinde "şems" geçen kelimeleri bul
            if target_root in clean_word:
                matches.append({
                    's': surah_num,
                    'a': verse_num,
                    'word': word,
                    'clean': clean_word,
                    'index': i
                })

# Gruplama ve Sayım
unique_verses = set()
total_count = 0

print(f"{'SURE':<20} | {'AYET':<5} | {'KELİME':<15} | {'TEMİZ':<15}")
print("-" * 65)

for m in matches:
    print(f"{m['s']:<20} | {m['a']:<5} | {m['word']:<15} | {m['clean']:<15}")
    unique_verses.add(f"{m['s']}:{m['a']}")
    total_count += 1

print("-" * 65)
print(f"\nTOPLAM BULUNAN SAYI: {total_count}")
print(f"FARKLI AYET SAYISI: {len(unique_verses)}")

# Detaylı İnceleme
print("\n--- Olası Yanlış Eşleşme Kontrolü ---")
for m in matches:
    w = m['clean']
    # "şems" ile bitmeyen veya başlamayan (ortada geçen) var mı?
    # Genelde: el-şems, ve-el-şems, bi-el-şems, li-el-şems
    # Hepsi "şems" ile bitmeli (zamir almadığı sürece).
    # Kuran'da güneşe zamir gelir mi? "Şemsu-ha" (Duha suresi 1: kuşluğu?) -> Şems'in kuşluğu olur mu? "Veş-şemsi ve duhaha" (Güneş'e ve onun aydınlığına).
    # Burada "duhaha"daki ha güneşe gider. Ama "Şems" kelimesinin kendisine zamir bitişik mi?
    # "Şemsuhum" ? Yok.
    
    if not w.endswith('شمس'):
         # Şems ile bitmeyen kelime var mı? (Belki zamir almış hali)
         print(f"UYARI: 'şems' ile bitmiyor -> {m['s']}:{m['a']} - {m['word']} ({w})")
