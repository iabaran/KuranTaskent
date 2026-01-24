#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Kur'an'da Musa (موسى) kelimesini detaylı inceleyen script
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

target_root = 'موسى'
matches = []

print("=" * 80)
print("MUSA (موسى) KELİMESİ DETAYLI ANALİZİ")
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
            
            # İçinde "Musa" geçen kelimeleri bul
            if target_root in clean_word:
                # Tam eşleşme veya ek almış halleri
                # Olası formlar: موسى (Musa), ياموسى (Ya Musa), بموسى (Bi Musa), لموسى (Li Musa), وموسى (Ve Musa), فموسى (Fe Musa)
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

# Kontrol: Acaba "Musa" harfleri sırasıyla geçen ama Musa olmayan kelime var mı?
# "El-Musevi", "Musevvim" (işaretlenmiş) vb.
# Kuran'da "Musevvin" (موسعون - Zenginler/Genişletenler) var, ama "Musa" kökü (Mim-Vav-Sin-Ye-Maksura) ile karışmaz.
# "Musa" -> موسى (Ye-Maksura ile biter, ama bazen Y harfi ile de yazılabilir mi? Hayır, Musa sabittir.)
# Tek potansiyel karışıklık: Kelime içinde geçen başka kökler.
# Analiz edelim: Bulunan kelimelerden ismi Musa olmayan var mı?

non_musa_candidates = []
for m in matches:
    w = m['clean']
    # Musa olmayanları filtrele (Manuel whitelist mantığı ile kontrol)
    # Musa formları: موسى, وموسى, ياموسى, بموسى, لموسى, فموسى, ال, موسى
    # Kendisi "موسى" ile bitiyorsa %99.9 Musa'dır.
    if not w.endswith('موسى'):
        non_musa_candidates.append(m)

if non_musa_candidates:
    print("\n⚠️ DİKKAT: 'Musa' ile bitmeyen adaylar (Kontrol Gerekli):")
    for m in non_musa_candidates:
         print(f"{m['s']}:{m['a']} - {m['word']} ({m['clean']})")
else:
    print("\n✅ Tüm eşleşmeler 'موسى' ile bitiyor, güvenilir görünüyor.")

print("\n")
