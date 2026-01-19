#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
أيام (günler) kelimesinin geçtiği 26 ayeti analiz eder
"""

import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('quran_arabic.json', 'r', encoding='utf-8') as f:
    quran = json.load(f)

def norm(t):
    return re.sub(r'[\u064B-\u065F\u0670\u06D6-\u06ED\u0640\u0653-\u0655]', '', t)

# Ayetleri bul ve Türkçe mealiyle listele
ayyam_verses = [
    (2, 80, "sayılı günler"),
    (2, 184, "sayılı günler / başka günlerde"),
    (2, 185, "başka günlerden"),
    (2, 196, "üç gün"),
    (2, 203, "sayılı günlerde"),
    (3, 24, "sayılı günler"),
    (3, 41, "üç gün"),
    (3, 140, "o günleri"),
    (5, 89, "üç gün"),
    (7, 54, "altı günde"),
    (10, 3, "altı günde"),
    (10, 102, "günlerini"),
    (11, 7, "altı günde"),
    (11, 65, "üç gün"),
    (22, 28, "belirli günlerde"),
    (25, 59, "altı günde"),
    (32, 4, "altı günde"),
    (34, 18, "günlerce"),
    (41, 10, "dört günde"),
    (41, 16, "uğursuz günlerde"),
    (45, 14, "Allah'ın günlerini"),
    (50, 38, "altı günde"),
    (57, 4, "altı günde"),
    (69, 7, "yedi gece sekiz gün"),
    (69, 24, "geçmiş günlerde"),
]

print("GÜNLER (أيام) - ANLAM ANALİZİ")
print("=" * 70)
print()

sayilir_gun = 0
belirsiz = 0

for i, (s, a, anlam) in enumerate(ayyam_verses, 1):
    # Sayilir gun mu?
    if any(x in anlam for x in ["gün", "günde", "günler", "günlerde", "günlerce"]):
        sayilir_gun += 1
        status = "✓ SAYILIR"
    else:
        belirsiz += 1
        status = "? BELİRSİZ"
    
    print(f"{i}. {s}:{a} - {anlam} [{status}]")

print()
print("=" * 70)
print(f"SAYILIR GÜN: {sayilir_gun}")
print(f"BELİRSİZ: {belirsiz}")
print(f"TOPLAM: {len(ayyam_verses)}")
