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

INVALID_FORMS = [
    'خللها', 'خلله', 'يضلله', 'وظللهم', 'ظلله', 
    'خللهما', 'ٱللهو', 'ظللها', 'ٱللهب', 'للهدى'
]

list_standard = []
list_allahumma = []
list_headers = []

# 1. VERSES
for surah in data:
    for verse in surah['verses']:
        clean_text = remove_diacritics(verse['text'])
        words = clean_text.split()
        
        for w in words:
            w_clean = re.sub(r'[^\w\s]', '', w)
            if 'الله' in w_clean or 'لله' in w_clean:
                if w_clean in INVALID_FORMS: continue
                if 'اللهم' in w_clean:
                    list_allahumma.append({'s': surah['id'], 'a': verse['id']})
                else:
                    list_standard.append({'s': surah['id'], 'a': verse['id']})

# 2. HEADERS
for s in range(1, 115):
    if s == 1: continue 
    if s == 9: continue 
    list_headers.append({'s': s, 'h': 1})

# Combine ALL for tooltip navigation
# We want user to see EVERY occurrence when they click.
full_list = list_headers + list_standard + list_allahumma
full_list.sort(key=lambda x: (x['s'], x.get('a', 0))) 

# Generate JS
js_content = "const allahData = [\n"
entries = []
for x in full_list:
    if 'h' in x:
        entries.append(f"{{s:{x['s']}, h:1}}")
    else:
        entries.append(f"{{s:{x['s']}, a:{x['a']}}}")

js_content += ", ".join(entries)
js_content += "\n];"

with open('allah_data.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"Generated allah_data.js with {len(full_list)} entries.")
print(f"Standard: {len(list_standard)}, Allahumma: {len(list_allahumma)}, Headers: {len(list_headers)}")
