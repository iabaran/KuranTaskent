#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import re

with open('quran_arabic.json', 'r', encoding='utf-8') as f:
    quran = json.load(f)

def normalize(text):
    return re.sub(r'[\u064B-\u065F\u0670\u06D6-\u06ED\u0640\u0653-\u0655]', '', text)

print("ARI (NAHL) Kelimesi Araması (Normalize edilmiş):")
print("-" * 40)

target = 'نحل' # Nahl

for surah in quran:
    for verse in surah['verses']:
        text = verse['text']
        clean = normalize(text)
        
        # Kelime bazlı arama
        words = clean.split()
        for w in words:
            # "Nahl" kelimesini ara
            # En-Nahl (الـنـحـل) -> والنحل, فالنحل
            if 'نحل' in w:
                print(f"Sure: {surah['name']} ({surah['id']}) - Ayet: {verse['id']}")
                print(f"Kelime: {w}")
                print(f"Metin: {text}")
                print("-" * 40)
