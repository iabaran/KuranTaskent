# -*- coding: utf-8 -*-
import json
import sys
import re

# Force UTF-8 for stdout
sys.stdout.reconfigure(encoding='utf-8')

# Load data
with open('quran_arabic.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def remove_diacritics(text):
    arabic_diacritics = re.compile(r'[\u064B-\u065F\u0670\u0617-\u061A\u06D6-\u06ED]')
    return arabic_diacritics.sub('', text)

def verify_word(word_root, display_name):
    print(f"\n========================================")
    print(f"VERIFICATION: {display_name} ({word_root})")
    print(f"========================================")
    
    total_count = 0
    occurrence_index = 1
    
    for surah in data:
        for verse in surah['verses']:
            clean = remove_diacritics(verse['text'])
            
            # Find all matches
            if word_root in clean:
                count = clean.count(word_root)
                for _ in range(count):
                    # Highlight the word in the cleaned text for display
                    highlighted = clean.replace(word_root, f"[{word_root}]")
                    # Or better, just print location
                    print(f"{occurrence_index}. {surah['name']} ({surah['id']}:{verse['id']})")
                    # print(f"   Text: {verse['text']}")
                    occurrence_index += 1
                total_count += count

    print(f"----------------------------------------")
    print(f"Total Found: {total_count}")
    print(f"========================================")
    return total_count

# Qamar (Moon) - قمر
count_qamar = verify_word('قمر', 'AY (Qamar)')

# Shams (Sun) - شمس
count_shams = verify_word('شمس', 'GUNES (Shams)')
