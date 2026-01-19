#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
GÜN kelimesini anlamsal olarak ayırır:
1. SAYILIR GÜN: 1 gün, 2 gün, 365 gün gibi - zaman birimi
2. O GÜN: يومئذ - zaman zarfı, belirli bir güne atıf

477 - 59 = 418 = 19 × 22
"""

import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('quran_arabic.json', 'r', encoding='utf-8') as f:
    quran = json.load(f)

def normalize(t):
    return re.sub(r'[\u064B-\u065F\u0670\u06D6-\u06ED\u0640\u0653-\u0655]', '', t)

# Kategoriler
# يومئذ = "o gün" - zaman zarfı (SAYILMAZ)
# يوم = "gün" - zaman birimi (SAYILIR)

yevmeizin_count = 0  # O gün (zaman zarfı)
yevm_countable = 0   # Sayılır gün (zaman birimi)
ayyam_count = 0      # Günler (çoğul)

yevmeizin_list = []
yevm_list = []
ayyam_list = []

for s in quran:
    for v in s.get('verses', []):
        for w in v['text'].split():
            nw = normalize(w)
            
            # 1. ÇOĞUL: أيام (günler) - sayılır
            if 'ايام' in nw or 'أيام' in nw:
                ayyam_count += 1
                ayyam_list.append({'s': s['id'], 'a': v['id'], 'w': w})
            
            # 2. يومئذ - "o gün" zaman zarfı - SAYILMAZ
            elif 'يومئذ' in nw:
                yevmeizin_count += 1
                yevmeizin_list.append({'s': s['id'], 'a': v['id'], 'w': w})
            
            # 3. يوم - sayılır gün (zaman birimi)
            elif 'يوم' in nw:
                yevm_countable += 1
                yevm_list.append({'s': s['id'], 'a': v['id'], 'w': w})

# Hesaplamalar
total_all = yevm_countable + yevmeizin_count + ayyam_count
sayilir_total = yevm_countable + ayyam_count

print("=" * 70)
print("GÜN KELİMESİ ANLAMSAL AYRIM")
print("=" * 70)

print(f"\n1. SAYILIR GÜN (يوم - zaman birimi): {yevm_countable}")
print(f"   Örnek: bir gün, iki gün, kıyamet günü, hesap günü...")

print(f"\n2. O GÜN (يومئذ - zaman zarfı): {yevmeizin_count}")
print(f"   'O günde', 'O gün' anlamında - belirli bir güne atıf")

print(f"\n3. GÜNLER (أيام - çoğul): {ayyam_count}")
print(f"   Birden fazla gün")

print("\n" + "=" * 70)
print("HESAPLAMA")
print("=" * 70)
print(f"\nToplam tüm 'gün' geçişleri: {total_all}")
print(f"Eksi 'O gün' (يومئذ) formu: -{yevmeizin_count}")
print(f"SAYILIR GÜN TOPLAMI: {sayilir_total}")

if sayilir_total % 19 == 0:
    print(f"\n✓ {sayilir_total} = 19 × {sayilir_total // 19}")
else:
    print(f"\n{sayilir_total} sayısı 19'un katı değil")
    print(f"En yakın 19 katı: {(sayilir_total // 19) * 19} veya {((sayilir_total // 19) + 1) * 19}")

# Detaylı dosya yaz
with open('yevm_semantic_analysis.txt', 'w', encoding='utf-8') as f:
    f.write("=" * 70 + "\n")
    f.write("GÜN KELİMESİ ANLAMSAL ANALİZ\n")
    f.write("=" * 70 + "\n\n")
    
    f.write("""Bu analiz, "gün" kelimesinin anlamsal ayrımını yapar:

1. SAYILIR GÜN (يوم): Zaman birimi olarak kullanılan "gün"
   - "bir gün", "yedi gün", "kıyamet günü" gibi
   - Sayılabilir, ölçülebilir zaman dilimi
   
2. O GÜN (يومئذ): Zaman zarfı olarak kullanılan "o gün"
   - "O günde şöyle olacak" gibi
   - Belirli bir güne atıf yapan ifade
   - Sayılabilir gün anlamı taşımaz

3. GÜNLER (أيام): Çoğul form
   - "Birkaç gün", "altı gün" gibi

""")
    
    f.write(f"\n{'='*70}\n")
    f.write("SONUÇ\n")
    f.write(f"{'='*70}\n\n")
    
    f.write(f"Sayılır gün (يوم): {yevm_countable}\n")
    f.write(f"O gün (يومئذ): {yevmeizin_count}\n")
    f.write(f"Günler (أيام): {ayyam_count}\n")
    f.write(f"\nToplam tüm formlar: {total_all}\n")
    f.write(f"Sayılır gün toplamı: {sayilir_total} (= {yevm_countable} + {ayyam_count})\n")
    
    if sayilir_total % 19 == 0:
        f.write(f"\n✓ {sayilir_total} = 19 × {sayilir_total // 19}\n")
    
    f.write(f"\n\n{'='*70}\n")
    f.write(f"SAYILIR GÜN LİSTESİ ({yevm_countable} adet)\n")
    f.write(f"{'='*70}\n")
    for i, item in enumerate(yevm_list, 1):
        f.write(f"{i}. {item['s']}:{item['a']} - {item['w']}\n")
    
    f.write(f"\n\n{'='*70}\n")
    f.write(f"O GÜN (يومئذ) LİSTESİ ({yevmeizin_count} adet)\n")
    f.write(f"{'='*70}\n")
    for i, item in enumerate(yevmeizin_list, 1):
        f.write(f"{i}. {item['s']}:{item['a']} - {item['w']}\n")
    
    f.write(f"\n\n{'='*70}\n")
    f.write(f"GÜNLER (أيام) LİSTESİ ({ayyam_count} adet)\n")
    f.write(f"{'='*70}\n")
    for i, item in enumerate(ayyam_list, 1):
        f.write(f"{i}. {item['s']}:{item['a']} - {item['w']}\n")

print("\nDetaylar: yevm_semantic_analysis.txt")
