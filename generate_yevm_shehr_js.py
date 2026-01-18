# -*- coding: utf-8 -*-
import json
import sys
import re

# Force UTF-8 for stdout
sys.stdout.reconfigure(encoding='utf-8')

with open('quran_arabic.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def remove_diacritics(text):
    text = re.sub(r'[\u064B-\u065F\u0670\u0617-\u061A\u06D6-\u06ED]', '', text)
    return text

# Exact singular forms to include
shehr_target_forms = ['شهر', 'ٱلشهر', 'شهرا', 'بٱلشهر', 'وٱلشهر']
yevm_target_forms = ['يوم', 'ٱليوم', 'ويوم', 'وٱليوم', 'يوما', 'ليوم', 'فٱليوم', 'بيوم', 'وبٱليوم', 'بٱليوم']

def get_occurrences_variants(target_forms, display_name):
    locs = []
    
    for surah in data:
        for verse in surah['verses']:
            clean = remove_diacritics(verse['text'])
            # Split by whitespace and remove punctuation attached to words if needed
            # But arabic tokens usually space separated.
            # Let's split and clean.
            words = clean.split()
            
            for w in words:
                # Remove common punctuation marks if attached
                w_clean = re.sub(r'[^\w\s]', '', w)
                
                if w_clean in target_forms:
                    locs.append({'s': surah['id'], 'a': verse['id']})

    print(f"Total {display_name}: {len(locs)}")
    return locs

shehr_locs = get_occurrences_variants(shehr_target_forms, 'Shehr')
yevm_locs = get_occurrences_variants(yevm_target_forms, 'Yevm')

def generate_js(var_name, locs):
    print(f"const {var_name} = [")
    lines = []
    # Sort
    locs.sort(key=lambda x: (x['s'], x['a']))
    
    # Simple dedupe if split logic found same word twice? 
    # (e.g. if a verse has "yevm ... yevm").
    # The count should ideally include duplicates if they are valid "words".
    # Yevm count 365 is usually total word count.
    
    for item in locs:
        lines.append(f"{{s:{item['s']}, a:{item['a']}}}")
    print(", ".join(lines))
    print("];")

generate_js('shehrData', shehr_locs)
generate_js('yevmData', yevm_locs)
