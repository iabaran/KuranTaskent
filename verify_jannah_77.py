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

# Excluded verses (Homographs: Jinn, Madness, Shield)
# Format: "surah:verse"
EXCLUDED_LOCATIONS = [
    # Jinn/Madness/Delilik
    "7:184",
    "23:25",
    "34:8",
    "34:46",
    "37:158", # Jinn
    "114:6",  # Jinn (Jinnati)
    
    # Shield (Kalkan)
    "58:16",
    "63:2",
    
    # Fetuses (Ajinnah)
    "53:32"
]

print("--- JANNAH (PARADISE/GARDEN) COUNT ANALYSIS ---")

jannah_list = []

for surah in data:
    for verse in surah['verses']:
        s_id = str(surah['id'])
        v_id = str(verse['id'])
        loc_key = f"{s_id}:{v_id}"
        
        clean_text = remove_diacritics(verse['text'])
        words = clean_text.split()
        
        for w in words:
            # Clean punctuation
            w_raw = w
            w = re.sub(r'[^\w\s]', '', w) # Remove punctuation like brackets
            
            # Match Target Forms
            is_match = False
            
            # 1. Standard Jannah (جنة) - ending with ta marbuta
            if w.endswith('جنة') or 'جنة' in w: # Covers al-jannah, bil-jannah
                # Must exclude if it's strictly a plural variant like 'jannatan' (dual) if we only want singular
                # But let's check exact suffix matches manually later or assume 'jannah' is unique enough
                is_match = True
            
            # 2. Possessive Forms (Open Ta)
            # Jannati (جنتي), Jannatuke (جنتك), Jannatehu (جنته)
            if w.endswith('جنتي') or w.endswith('جنتك') or w.endswith('جنته'):
                is_match = True
                
            if is_match:
                # Check exclusions
                if loc_key in EXCLUDED_LOCATIONS:
                    # Special check: Does the verse have BOTH a valid and invalid one?
                    # Saffat 37:158 has Jinn only.
                    # 7:184 has Madness only.
                    # Rare case: A verse has Jannah AND Jinna?
                    # Let's log it as excluded.
                    # print(f"Excluded: {loc_key} ({w})")
                    pass
                else:
                    # Valid Match?
                    # Check for 'Jannatan' (Dual) - 55:46, 55:62 -> جنتان
                    # Check for Plurals 'Jannat' -> جنات
                    
                    if 'جنات' in w: # Plural
                        continue
                        
                    if 'جنتان' in w or 'جنتين' in w: # Dual
                        continue
                        
                    # Add to list
                    jannah_list.append({
                        's': surah['id'],
                        'a': verse['id'],
                        'w': w_raw
                    })

# Print Results
print(f"Total Count: {len(jannah_list)}")

# Generate JS Data
print("\nJS DATA (jannahData):")
print("-" * 20)
js_entries = []
for item in jannah_list:
    js_entries.append(f"{{s:{item['s']}, a:{item['a']}}}")
print(", ".join(js_entries))


# --- JAHANNAM ANALYSIS ---
print("\n\n--- JAHANNAM (HELL) COUNT ANALYSIS ---")
jahannam_list = []
for surah in data:
    for verse in surah['verses']:
        clean_text = remove_diacritics(verse['text'])
        if 'جهنم' in clean_text:
            cnt = clean_text.count('جهنم')
            for _ in range(cnt):
                jahannam_list.append({
                    's': surah['id'],
                    'a': verse['id']
                })
print(f"Total Count: {len(jahannam_list)}")

print("\nJS DATA (jahannamData):")
print("-" * 20)
js_entries_j = []
for item in jahannam_list:
    js_entries_j.append(f"{{s:{item['s']}, a:{item['a']}}}")
print(", ".join(js_entries_j))
