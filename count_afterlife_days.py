#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Ahiretle ilgili gün ifadelerini sayar:
- يوم الدين (Din Günü)
- يوم القيامة (Kıyamet Günü)
- يوم الحشر (Mahşer Günü)
- يوم الحساب (Hesap Günü)
"""

import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('quran_arabic.json', 'r', encoding='utf-8') as f:
    quran = json.load(f)

def norm(t):
    return re.sub(r'[\u064B-\u065F\u0670\u06D6-\u06ED\u0640\u0653-\u0655]', '', t)

categories = {
    'din': {'name': 'Din Günü (يوم الدين)', 'pattern': 'دين', 'count': 0, 'verses': []},
    'qiyama': {'name': 'Kıyamet Günü (يوم القيامة)', 'pattern': 'قيامة', 'count': 0, 'verses': []},
    'hashr': {'name': 'Mahşer Günü (يوم الحشر)', 'pattern': 'حشر', 'count': 0, 'verses': []},
    'hisab': {'name': 'Hesap Günü (يوم الحساب)', 'pattern': 'حساب', 'count': 0, 'verses': []},
    'akhira': {'name': 'Ahiret (الآخرة)', 'pattern': 'اخرة', 'count': 0, 'verses': []},
    'fasl': {'name': 'Ayrım Günü (يوم الفصل)', 'pattern': 'فصل', 'count': 0, 'verses': []},
}

for s in quran:
    for v in s.get('verses', []):
        text = v['text']
        ntext = norm(text)
        ref = f"{s['id']}:{v['id']}"
        
        # يوم الدين
        if 'دين' in ntext and 'يوم' in ntext:
            categories['din']['count'] += 1
            categories['din']['verses'].append(ref)
        
        # يوم القيامة
        if 'قيمة' in ntext or 'قيامة' in ntext:
            categories['qiyama']['count'] += 1
            categories['qiyama']['verses'].append(ref)
        
        # الحشر
        if 'حشر' in ntext:
            categories['hashr']['count'] += 1
            categories['hashr']['verses'].append(ref)
        
        # الحساب
        if 'حساب' in ntext:
            categories['hisab']['count'] += 1
            categories['hisab']['verses'].append(ref)
        
        # الآخرة
        if 'اخرة' in ntext or 'آخرة' in ntext:
            categories['akhira']['count'] += 1
            categories['akhira']['verses'].append(ref)
        
        # الفصل - sadece يوم ile birlikte
        if 'فصل' in ntext and 'يوم' in ntext:
            categories['fasl']['count'] += 1
            categories['fasl']['verses'].append(ref)

print("=" * 60)
print("AHİRET İLE İLGİLİ İFADELER")
print("=" * 60)

total = 0
for key, data in categories.items():
    if data['count'] > 0:
        print(f"\n{data['name']}: {data['count']}")
        print(f"   İlk 5 ayet: {', '.join(data['verses'][:5])}")
        total += data['count']

print("\n" + "=" * 60)
print(f"TOPLAM (tekrarsız değil): {total}")
