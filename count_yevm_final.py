#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Kur'an'da GÜN anlamına gelen kelimeleri DOĞRU şekilde sayar.
أيام (eyyam/günler) ile صيام (sıyam/oruç), قيام (kıyam/kalkış) vs. karıştırmaz.
"""

import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('quran_arabic.json', 'r', encoding='utf-8') as f:
    quran = json.load(f)

def normalize(t):
    return re.sub(r'[\u064B-\u065F\u0670\u06D6-\u06ED\u0640\u0653-\u0655]', '', t)

# GÜN kelimeleri
# TEKİL: يوم (yevm)
# ÇOĞUL: أيام (eyyam) - dikkat: أ ile başlar

yevm_count = 0
ayyam_count = 0

yevm_list = []
ayyam_list = []

yevm_forms = {}
ayyam_forms = {}

for s in quran:
    for v in s.get('verses', []):
        for w in v['text'].split():
            nw = normalize(w)
            
            # TEKİL: يوم
            if 'يوم' in nw:
                yevm_count += 1
                yevm_list.append({'s': s['id'], 'a': v['id'], 'w': w})
                if w not in yevm_forms:
                    yevm_forms[w] = 0
                yevm_forms[w] += 1
            
            # ÇOĞUL: أيام - must start with أ or ا followed by يام
            # The normalized form should be ايام
            elif 'ايام' in nw or 'أيام' in nw:
                ayyam_count += 1
                ayyam_list.append({'s': s['id'], 'a': v['id'], 'w': w})
                if w not in ayyam_forms:
                    ayyam_forms[w] = 0
                ayyam_forms[w] += 1

print("=" * 60)
print("GÜN KELİMESİ KESİN SAYIM")
print("=" * 60)

print(f"\nTEKİL (يوم - yevm):")
for word, count in sorted(yevm_forms.items(), key=lambda x: -x[1])[:10]:
    print(f"  {word}: {count}")
if len(yevm_forms) > 10:
    print(f"  ... ve {len(yevm_forms)-10} form daha")
print(f"  TOPLAM TEKİL: {yevm_count}")

print(f"\nÇOĞUL (أيام - eyyam/günler):")
for word, count in sorted(ayyam_forms.items(), key=lambda x: -x[1]):
    print(f"  {word}: {count}")
print(f"  TOPLAM ÇOĞUL: {ayyam_count}")

print("\n" + "-" * 60)
print(f"GENEL TOPLAM (GÜN): {yevm_count + ayyam_count}")
print("-" * 60)

# Write detailed file
with open('yevm_final_count.txt', 'w', encoding='utf-8') as f:
    f.write("GÜN KELİMESİ KESİN SAYIM\n")
    f.write("=" * 60 + "\n\n")
    
    f.write(f"TEKİL (يوم - yevm): {yevm_count}\n")
    f.write(f"ÇOĞUL (أيام - eyyam): {ayyam_count}\n")
    f.write(f"TOPLAM: {yevm_count + ayyam_count}\n\n")
    
    f.write("FORM DAĞILIMI:\n")
    f.write("-" * 40 + "\n")
    for word, count in sorted(yevm_forms.items(), key=lambda x: -x[1]):
        f.write(f"  {word}: {count}\n")
    f.write("\n")
    for word, count in sorted(ayyam_forms.items(), key=lambda x: -x[1]):
        f.write(f"  {word}: {count}\n")
    
    f.write(f"\n\nTEKİL AYETLER ({yevm_count}):\n")
    for i, item in enumerate(yevm_list, 1):
        f.write(f"{i}. {item['s']}:{item['a']} - {item['w']}\n")
    
    f.write(f"\n\nÇOĞUL AYETLER ({ayyam_count}):\n")
    for i, item in enumerate(ayyam_list, 1):
        f.write(f"{i}. {item['s']}:{item['a']} - {item['w']}\n")

print("\nDetaylar: yevm_final_count.txt")
