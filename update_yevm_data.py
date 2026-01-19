#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
GÜN verisi için JS dosyası oluşturur.
Sadece SAYILAN günleri içerir (يومئذ ve قيوم hariç)
"""

import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('quran_arabic.json', 'r', encoding='utf-8') as f:
    quran = json.load(f)

def norm(t):
    return re.sub(r'[\u064B-\u065F\u0670\u06D6-\u06ED\u0640\u0653-\u0655]', '', t)

yevm_list = []  # Sayılır gün (tekil)
ayyam_list = []  # Günler (çoğul)

for s in quran:
    for v in s.get('verses', []):
        for w in v['text'].split():
            nw = norm(w)
            
            # Çoğul: أيام
            if 'ايام' in nw or 'أيام' in nw:
                ayyam_list.append({'s': s['id'], 'a': v['id'], 'w': w})
            # Kayyum - ÇIKARILIR
            elif 'قيوم' in nw:
                pass
            # O gün (يومئذ) - ÇIKARILIR
            elif 'يومئذ' in nw:
                pass
            # Sayılır gün
            elif 'يوم' in nw:
                yevm_list.append({'s': s['id'], 'a': v['id'], 'w': w})

# JS dosyası oluştur
js_content = f"""// Gün (Yevm) Verileri
// SAYILAN: Tekil (يوم) + Çoğul (أيام) = {len(yevm_list)} + {len(ayyam_list)} = {len(yevm_list) + len(ayyam_list)}
// ÇIKARILAN: يومئذ (O gün - zaman zarfı): 70 | قيوم (Kayyum - Allah'ın sıfatı): 3

const yevmData = {json.dumps(yevm_list + ayyam_list, ensure_ascii=False)};
"""

with open('shams_qamar_yevm_shehr_data.js', 'r', encoding='utf-8') as f:
    old_content = f.read()

# Yevm verisini güncelle
new_content = re.sub(
    r'// Gün \(Yevm\).*?const yevmData = \[.*?\];',
    js_content.strip(),
    old_content,
    flags=re.DOTALL
)

with open('shams_qamar_yevm_shehr_data.js', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"Tekil (يوم): {len(yevm_list)}")
print(f"Çoğul (أيام): {len(ayyam_list)}")
print(f"TOPLAM: {len(yevm_list) + len(ayyam_list)}")
print("Dosya güncellendi: shams_qamar_yevm_shehr_data.js")
