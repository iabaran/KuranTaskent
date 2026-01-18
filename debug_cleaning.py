import json
import re

with open('quran_arabic.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Check 2:30 for Malaika
s2 = next(s for s in data if s['id'] == 2)
v30 = next(v for v in s2['verses'] if v['id'] == 30)

text = v30['text']
print(f"Original 2:30: {text}")

def remove_diacritics(text):
    return re.sub(r'[\u064B-\u065F\u0670]', '', text)

cleaned = remove_diacritics(text)
print(f"Cleaned 2:30: {cleaned}")
words = cleaned.split()
print("Words:", words)

# Check specifically for 'Malaika' skeleton
# Expecting: للملائكة -> skeleton 'للملائك' or 'للملائكة' depending on Ta Marbuta
# If my script expects 'ملائك' substring, it should find it.

print("\n--- Testing Logic ---")
w_clean = "للملائكة" # example
if 'ملائك' in w_clean:
    print(f"Match found in {w_clean}")
else:
    print(f"No match in {w_clean}")
