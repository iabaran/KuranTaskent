#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import re

with open('quran_arabic.json', 'r', encoding='utf-8') as f:
    quran = json.load(f)

def normalize(text):
    return re.sub(r'[\u064B-\u065F\u0670\u06D6-\u06ED\u0640\u0653-\u0655]', '', text)

print(f"{'SURE':<5} | {'AYET':<5} | {'KELİME':<20} | {'TEMİZ':<20}")
print("-" * 60)

count = 0

for surah in quran:
    for verse in surah['verses']:
        text = verse['text']
        words = text.split()
        
        for w in words:
            clean = normalize(w)
            
            if 'ظل' in clean:
                if 'ظلم' in clean or 'ظال' in clean or 'مظل' in clean:
                    continue
                if 'أظلم' in clean:
                    continue

                print(f"{surah['id']:<5} | {verse['id']:<5} | {w:<20} | {clean:<20}")
                count += 1

print("-" * 60)
print(f"Toplam Aday Sayısı: {count}")
