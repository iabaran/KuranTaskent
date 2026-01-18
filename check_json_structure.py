# -*- coding: utf-8 -*-
import json
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Load JSON
with open('quran_arabic.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Type: {type(data)}")
print(f"Length: {len(data)}")
print(f"\nFirst item keys: {list(data[0].keys())}")
print(f"\nFirst surah sample:")
for key, value in data[0].items():
    if isinstance(value, str):
        print(f"  {key}: {value[:100]}")
    elif isinstance(value, list):
        print(f"  {key}: List with {len(value)} items")
        if len(value) > 0:
            print(f"    First item: {str(value[0])[:100]}")
    else:
        print(f"  {key}: {value}")
