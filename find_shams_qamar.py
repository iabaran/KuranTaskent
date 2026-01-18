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

def get_occurrences_exact(word_root, display_name):
    locs = []
    total_count = 0
    
    print(f"\nANALYZE: {display_name} ({word_root})")
    print("-" * 40)
    
    for surah in data:
        for verse in surah['verses']:
            clean = remove_diacritics(verse['text'])
            
            if word_root in clean:
                count = clean.count(word_root)
                total_count += count
                for _ in range(count):
                    locs.append({'s': surah['id'], 'a': verse['id']})
                    # Avoid printing arabic to console if it causes issues, or sanitize
                    # print(f"{surah['id']}:{verse['id']}") 

    print(f"Total Count: {total_count}")
    return locs

# Shams (Sun) - شمس
shams_locs = get_occurrences_exact('شمس', 'GUNES (Shams)')

# Qamar (Moon) - قمر
qamar_locs = get_occurrences_exact('قمر', 'AY (Qamar)')

# Generate JS data directly
print("\nJS DATA GENERATION")
print("-" * 40)

def generate_js(var_name, locs):
    print(f"const {var_name} = [")
    lines = []
    # Sort
    locs.sort(key=lambda x: (x['s'], x['a']))
    
    for item in locs:
        lines.append(f"{{s:{item['s']}, a:{item['a']}}}")
    print(", ".join(lines))
    print("];")

generate_js('shamsData', shams_locs)
generate_js('qamarData', qamar_locs)
