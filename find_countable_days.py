#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Sayılabilir gün ifadelerini bulur:
- "bir gün", "iki gün", "üç gün" gibi
- "kaç gün", "hangi gün" gibi
- "yedi gece sekiz gün" gibi

Ahiret günü, kıyamet günü gibi genel ifadeler DEĞİL
"""

import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('quran_arabic.json', 'r', encoding='utf-8') as f:
    quran = json.load(f)

def norm(t):
    return re.sub(r'[\u064B-\u065F\u0670\u06D6-\u06ED\u0640\u0653-\u0655]', '', t)

# Sayı içeren gün ifadeleri için Arapça kalıplar
# يوماً (bir gün/gün olarak), ثلاثة أيام (üç gün), ستة أيام (altı gün)
# يومين (iki gün), أربعة أيام (dört gün), سبع ليال وثمانية أيام (yedi gece sekiz gün)

counted_day_verses = []

# Sayılar
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

for s in quran:
    for v in s.get('verses', []):
        text = v['text']
        ntext = norm(text)
        
        # يومين (iki gün) - özel form
        if 'يومين' in ntext:
            counted_day_verses.append({
                's': s['id'],
                'a': v['id'],
                'type': 'iki gün (يومين)',
                'text': text[:80]
            })
        
        # Sayı + أيام (günler)
        for num_ar, num_val in numbers_ar.items():
            if norm(num_ar) in ntext and ('ايام' in ntext or 'أيام' in ntext):
                counted_day_verses.append({
                    's': s['id'],
                    'a': v['id'],
                    'type': f'{num_val} gün ({num_ar} أيام)',
                    'text': text[:80]
                })
                break
        
        # يوماً veya يوما (bir gün - belirsiz)
        if 'يوما' in ntext and 'يومئذ' not in ntext:
            # "Bir gün mü kaldın" gibi ifadeler
            words = text.split()
            for w in words:
                nw = norm(w)
                if nw == 'يوما':
                    counted_day_verses.append({
                        's': s['id'],
                        'a': v['id'],
                        'type': 'bir gün/gün olarak (يوماً)',
                        'text': text[:80]
                    })
                    break

# Tekrar eden ayetleri temizle
seen = set()
unique_verses = []
for v in counted_day_verses:
    key = f"{v['s']}:{v['a']}"
    if key not in seen:
        seen.add(key)
        unique_verses.append(v)

print("SAYILIR GÜN İFADELERİ (kaç gün, bir gün, vb.)")
print("=" * 70)
print()

for i, v in enumerate(unique_verses, 1):
    print(f"{i}. {v['s']}:{v['a']} - {v['type']}")
    print(f"   {v['text']}...")
    print()

print("=" * 70)
print(f"TOPLAM: {len(unique_verses)} ayet")
