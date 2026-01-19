#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Ahiretle ilgili gün ifadelerinin JS veri dosyasını oluşturur
"""

import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('quran_arabic.json', 'r', encoding='utf-8') as f:
    quran = json.load(f)

def norm(t):
    return re.sub(r'[\u064B-\u065F\u0670\u06D6-\u06ED\u0640\u0653-\u0655]', '', t)

# Kategoriler
din_data = []       # يوم الدين
qiyama_data = []    # يوم القيامة
hashr_data = []     # الحشر
hisab_data = []     # الحساب
fasl_data = []      # يوم الفصل

for s in quran:
    for v in s.get('verses', []):
        text = v['text']
        ntext = norm(text)
        ref = {'s': s['id'], 'a': v['id']}
        
        # يوم الدين
        if 'دين' in ntext and 'يوم' in ntext:
            ref_copy = ref.copy()
            ref_copy['w'] = 'يوم الدين'
            din_data.append(ref_copy)
        
        # يوم القيامة
        if 'قيمة' in ntext or 'قيامة' in ntext:
            ref_copy = ref.copy()
            ref_copy['w'] = 'يوم القيامة'
            qiyama_data.append(ref_copy)
        
        # الحشر
        if 'حشر' in ntext:
            ref_copy = ref.copy()
            ref_copy['w'] = 'الحشر'
            hashr_data.append(ref_copy)
        
        # الحساب
        if 'حساب' in ntext:
            ref_copy = ref.copy()
            ref_copy['w'] = 'الحساب'
            hisab_data.append(ref_copy)
        
        # الفصل - sadece يوم ile birlikte
        if 'فصل' in ntext and 'يوم' in ntext:
            ref_copy = ref.copy()
            ref_copy['w'] = 'يوم الفصل'
            fasl_data.append(ref_copy)

# JS dosyası oluştur
js_content = f"""
// Ahiret ile ilgili gün ifadeleri

// Din Günü (يوم الدين) - {len(din_data)}
const dinGunuData = {json.dumps(din_data, ensure_ascii=False)};

// Kıyamet Günü (يوم القيامة) - {len(qiyama_data)}
const qiyamaGunuData = {json.dumps(qiyama_data, ensure_ascii=False)};

// Mahşer Günü (الحشر) - {len(hashr_data)}
const hashrGunuData = {json.dumps(hashr_data, ensure_ascii=False)};

// Hesap Günü (الحساب) - {len(hisab_data)}
const hisabGunuData = {json.dumps(hisab_data, ensure_ascii=False)};

// Ayrım Günü (يوم الفصل) - {len(fasl_data)}
const faslGunuData = {json.dumps(fasl_data, ensure_ascii=False)};
"""

with open('afterlife_days_data.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"Din Günü: {len(din_data)}")
print(f"Kıyamet Günü: {len(qiyama_data)}")
print(f"Mahşer Günü: {len(hashr_data)}")
print(f"Hesap Günü: {len(hisab_data)}")
print(f"Ayrım Günü: {len(fasl_data)}")
print("\nDosya oluşturuldu: afterlife_days_data.js")
