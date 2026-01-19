#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
31 sayılabilir gün ifadesini JS veri dosyasına ekler
"""

import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('quran_arabic.json', 'r', encoding='utf-8') as f:
    quran = json.load(f)

def norm(t):
    return re.sub(r'[\u064B-\u065F\u0670\u06D6-\u06ED\u0640\u0653-\u0655]', '', t)

numbers_ar = {
    'واحد': 1, 'أحد': 1,
    'اثنين': 2, 'يومين': 2,
    'ثلاث': 3, 'ثلٰث': 3,
    'أربع': 4, 'اربع': 4,
    'خمس': 5,
    'ست': 6,
    'سبع': 7,
    'ثمان': 8, 'ثماني': 8,
    'تسع': 9,
    'عشر': 10,
    'ألف': 1000,
    'خمسين': 50,
}

yevm_data = []
seen = set()

for s in quran:
    for v in s.get('verses', []):
        text = v['text']
        ntext = norm(text)
        key = f"{s['id']}:{v['id']}"
        
        if key in seen:
            continue
        
        # يومين (iki gün)
        if 'يومين' in ntext:
            yevm_data.append({'s': s['id'], 'a': v['id'], 'w': 'يومين'})
            seen.add(key)
            continue
        
        # Sayı + أيام (günler)
        found = False
        for num_ar, num_val in numbers_ar.items():
            if norm(num_ar) in ntext and ('ايام' in ntext or 'أيام' in ntext):
                yevm_data.append({'s': s['id'], 'a': v['id'], 'w': num_ar + ' أيام'})
                seen.add(key)
                found = True
                break
        
        if found:
            continue
        
        # يوماً veya يوما (bir gün)
        if 'يوما' in ntext and 'يومئذ' not in ntext:
            words = text.split()
            for w in words:
                nw = norm(w)
                if nw == 'يوما':
                    yevm_data.append({'s': s['id'], 'a': v['id'], 'w': 'يوماً'})
                    seen.add(key)
                    break

# Mevcut dosyayı oku
with open('shams_qamar_yevm_shehr_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Yevm verisini güncelle
new_yevm = f"""// Gün (Yevm) Verileri - Sayılabilir Gün İfadeleri
// 31 ayet = 1 aydaki gün sayısı
// Sadece "bir gün", "altı gün", "kaç gün" gibi sayılabilir ifadeler
// Hariç tutulan: يومئذ (O gün - zaman zarfı), قيوم (Kayyum - Allah'ın sıfatı), ahiret günü gibi genel ifadeler

const yevmData = {json.dumps(yevm_data, ensure_ascii=False)};"""

# Eski yevmData'yı değiştir
content = re.sub(
    r'// Gün \(Yevm\).*?const yevmData = \[.*?\];',
    new_yevm,
    content,
    flags=re.DOTALL
)

with open('shams_qamar_yevm_shehr_data.js', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Toplam: {len(yevm_data)} ayet")
print("Dosya güncellendi: shams_qamar_yevm_shehr_data.js")
