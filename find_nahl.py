#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import re

with open('quran_arabic.json', 'r', encoding='utf-8') as f:
    quran = json.load(f)

print("ARI (NAHL) Kelimesi Araması:")
print("-" * 40)

for surah in quran:
    for verse in surah['verses']:
        if 'نحل' in verse['text'] or 'النحل' in verse['text']:
            print(f"Sure: {surah['name']} ({surah['id']}) - Ayet: {verse['id']}")
            print(f"Metin: {verse['text']}")
            print("-" * 40)
