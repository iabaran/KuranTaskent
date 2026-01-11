#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kuran JSON veritabanını indir
"""

import requests
import json

print("Kuran metni indiriliyor...")

url = "https://raw.githubusercontent.com/risan/quran-json/master/dist/quran.json"
response = requests.get(url)

if response.status_code == 200:
    quran_data = response.json()
    
    # Kaydet
    with open("quran_arabic.json", "w", encoding="utf-8") as f:
        json.dump(quran_data, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] Kuran metni indirildi: quran_arabic.json")
    print(f"[OK] Toplam sure: {len(quran_data)}")
    
    # Örnek göster
    if len(quran_data) > 0:
        first_surah = quran_data[0]
        print(f"\nOrnek - Sure 1: {first_surah.get('name', 'N/A')}")
        print(f"Ayet sayisi: {len(first_surah.get('verses', []))}")
else:
    print(f"[HATA] Indirme basarisiz: {response.status_code}")
