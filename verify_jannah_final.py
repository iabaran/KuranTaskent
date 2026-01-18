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

EXCLUDED_LOCATIONS = [
    "7:184", "23:25", "34:8", "34:46", "37:158", "114:6", # Jinn/Delilik
    "58:16", "63:2", # Kalkan
    "53:32" # Ajinnah
]

print("--- JANNAH (PARADISE) FINAL VERIFICATION ---")

jannah_list = []

for surah in data:
    for verse in surah['verses']:
        s_id = str(surah['id'])
        v_id = str(verse['id'])
        loc_key = f"{s_id}:{v_id}"
        
        clean_text = remove_diacritics(verse['text'])
        words = clean_text.split()
        
        for w in words:
            w_clean = re.sub(r'[^\w\s]', '', w) # Remove punctuation
            
            is_valid = False
            
            # 1. Standard Singular (ending with ta marbuta) & Possessives
            # Matches: Jannah, Al-Jannah, Bil-Jannah, Jannati, Jannatehu...
            if 'جنة' in w_clean:
                 is_valid = True
            
            # 2. Open Ta Variant (Vakia 89)
            if w_clean.endswith('جنت') and 'جنت' in w_clean:
                # Be careful not to include Plurals (Jannat)
                # Vakia 89 is singular.
                if s_id == '56' and v_id == '89':
                    is_valid = True
            
            # 3. Dual Forms (Jannatan, Jannatayn)
            if 'جنتان' in w_clean or 'جنتين' in w_clean:
                is_valid = True
                
            if is_valid:
                # Exclusions
                if loc_key in EXCLUDED_LOCATIONS:
                    continue
                
                # Exclude Plurals (Jannat) containing 'aat'
                # but NOT Duals
                if 'جنات' in w_clean:
                    continue
                
                jannah_list.append({
                    's': surah['id'],
                    'a': verse['id']
                })

# Remove duplicates if any (though word-by-word shouldn't have dups unless mult occurrences)
# But we count OCCURRENCES, so duplicates in same verse are valid (e.g. 2 instances).
# Wait, are there verses with multiple Jannahs?
# 2:265 one, 2:266 one.
# Kehf 32-40 range.
# Let's trust the list.

print(f"Total Jannah Count: {len(jannah_list)}")

print("\n--- JAHANNAM (HELL) FINAL VERIFICATION ---")
jahannam_list = []
for surah in data:
    for verse in surah['verses']:
        clean_text = remove_diacritics(verse['text'])
        if 'جهنم' in clean_text:
            cnt = clean_text.count('جهنم')
            for _ in range(cnt):
                jahannam_list.append({'s': surah['id'], 'a': verse['id']})
                
print(f"Total Jahannam Count: {len(jahannam_list)}")

# Generate Output
print("\nJS Arrays:")
print("const jannahData = [")
entries = [f"{{s:{x['s']}, a:{x['a']}}}" for x in jannah_list]
print(", ".join(entries))
print("];")

print("const jahannamData = [")
entries_j = [f"{{s:{x['s']}, a:{x['a']}}}" for x in jahannam_list]
print(", ".join(entries_j))
print("];")
