import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('quran_arabic.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Inspect 1:1 and 1:3
for surah in data:
    if surah['id'] == 1:
        for verse in surah['verses']:
            if verse['id'] in [1, 3]:
                print(f"Verse {surah['id']}:{verse['id']}:")
                print(f"Raw: {ascii(verse['text'])}")
                print(f"Text: {verse['text']}")
