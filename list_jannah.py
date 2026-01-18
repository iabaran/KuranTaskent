# -*- coding: utf-8 -*-
import json
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('quran_arabic.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def remove_diacritics(text):
    text = re.sub(r'[\u064B-\u065F\u0670\u0617-\u061A\u06D6-\u06ED]', '', text)
    return text

def list_jannah_occurrences():
    print("--- JANNAH (جنة) OCCURRENCES ---")
    count = 0
    count_without_ajinnah = 0
    
    # Exclude 'ajinnah' (أجنة) explicitly
    
    for surah in data:
        for verse in surah['verses']:
            clean = remove_diacritics(verse['text'])
            # Find words containing j-n-h rooted sequence
            # Specifically 'jannah', 'al-jannah' etc.
            
            words = clean.split()
            for w in words:
                w_clean = re.sub(r'[^\w\s]', '', w)
                if 'جنة' in w_clean:
                    # Check if it is Ajinnah (fetuses) - Surah 53:32
                    if 'أجنة' in w_clean:
                        print(f"SKIPPED (Ajinnah): {surah['id']}:{verse['id']} - {w_clean}")
                        continue
                        
                    count_without_ajinnah += 1
                    print(f"{count_without_ajinnah}. {surah['id']}:{verse['id']} - {w_clean}")

list_jannah_occurrences()
