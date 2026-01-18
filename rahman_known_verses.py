# -*- coding: utf-8 -*-
"""
Rahman kelimesini API'den kontrol et
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Bilinen Rahman ayetleri (19 Mucizesi'nden)
# Rahman kelimesi 57 kez geçer (19x3)
known_rahman_verses = [
    (1, 1), (1, 3),  # Fatiha
    (2, 163),  # Bakara
    (13, 30), (17, 110), (19, 18), (19, 26), (19, 44), (19, 45), (19, 58), (19, 61), (19, 69), (19, 75), (19, 78), (19, 85), (19, 87), (19, 88), (19, 91), (19, 92), (19, 93), (19, 96),
    (20, 5), (20, 90), (20, 108), (20, 109),
    (21, 26), (21, 36), (21, 42), (21, 112),
    (25, 26), (25, 59), (25, 60), (25, 63),
    (26, 5),
    (27, 30),
    (36, 11), (36, 15), (36, 23), (36, 52),
    (41, 2),
    (43, 17), (43, 19), (43, 20), (43, 33), (43, 36), (43, 45), (43, 81),
    (50, 33),
    (55, 1),
    (59, 22),
    (78, 37), (78, 38)
]

print(f"Bilinen Rahman ayetleri: {len(known_rahman_verses)}")
print("\nJavaScript array:")
print("const rahmanData = [")
for i, (s, a) in enumerate(known_rahman_verses):
    comma = "," if i < len(known_rahman_verses) - 1 else ""
    print(f"    {{ s: {s}, a: {a} }}{comma}")
print("];")
print(f"\n// Toplam: {len(known_rahman_verses)} Rahman (19 x 3 = 57)")
