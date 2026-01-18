import json
import re
import sys

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

with open('quran_arabic.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Check 2:30
s2 = next(s for s in data if s['id'] == 2)
v30 = next(v for v in s2['verses'] if v['id'] == 30)

text = v30['text']
print(f"Original 2:30: {text}")

def remove_diacritics(text):
    # Expanded range to include more marks potentially?
    # 0610-061A (Control chars), 06D6-06ED (Quranic marks)
    # But let's stick to strict diacritics first.
    return re.sub(r'[\u064B-\u065F\u0670]', '', text)

cleaned = remove_diacritics(text)
print(f"Cleaned 2:30: {cleaned}")

words = cleaned.split()
for i, w in enumerate(words):
    print(f"Word {i}: {w} | Hex: {[hex(ord(c)) for c in w]}")
    # Inspect "Malaika"
    if 'للملائك' in w:
         print("MATCH FOUND in loop")

print("\n--- Manual Check ---")
target = 'شيطان'
s2v36 = next(v for v in s2['verses'] if v['id'] == 36) # Mention of Satan
text_satan = s2v36['text']
cleaned_satan = remove_diacritics(text_satan)
print(f"Satan Verse Cleaned: {cleaned_satan}")
for w in cleaned_satan.split():
    if target in w:
         print(f"Found {target} in {w}")
    else:
         # Print what it looks like if it resembles it
         if 'ش' in w and 'ط' in w:
             print(f"Potential mismatch: {w} | Hex: {[hex(ord(c)) for c in w]}")
