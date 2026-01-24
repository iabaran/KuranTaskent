#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import re

with open('quran_arabic.json', 'r', encoding='utf-8') as f:
    quran = json.load(f)

def normalize(text):
    return re.sub(r'[\u064B-\u065F\u0670\u06D6-\u06ED\u0640\u0653-\u0655]', '', text)

js_data = []
count = 0

print(f"{'SURE':<5} | {'AYET':<5} | {'KELİME':<20}")
print("-" * 40)

for surah in quran:
    for verse in surah['verses']:
        text = verse['text']
        words = text.split()
        
        for w in words:
            clean = normalize(w)
            
            if 'ظل' in clean:
                # 1. ZULÜM (Z-L-M) Kökü Filtreleri
                # 'ظلم', 'ظال' (Zalim), 'مظل' (Muzlim)
                if 'ظلم' in clean or 'ظال' in clean or 'مظل' in clean:
                    continue
                # 2. Özel Durumlar (Zallam, Zalum - Vav'lı formlar)
                # Script outputunda gördüğümüz 3 hatalı kelime:
                # 3:182 (Bi-Zallam), 14:34 (Le-Zalum), 33:72 (Zalumen)
                if clean in ['بظلام', 'لظلوم', 'ظلوما']:
                    continue
                
                # Diğer potansiyel kaçaklar (Zulmani vb)
                if 'ظلام' in clean: # Zallam
                   continue

                # Eşleşme
                # KuranOkuyucu formatı: {s: 1, a: 1, w: "kelime"}
                print(f"{surah['id']:<5} | {verse['id']:<5} | {w:<20}")
                js_data.append({
                    "s": surah['id'],
                    "a": verse['id'],
                    "w": w
                })
                count += 1

print("-" * 40)
print(f"Toplam: {count}")

# JS Dosyası Oluştur
js_content = f"const zilData = {json.dumps(js_data, ensure_ascii=False)};"
with open('zil_data.js', 'w', encoding='utf-8') as f:
    f.write(js_content)
