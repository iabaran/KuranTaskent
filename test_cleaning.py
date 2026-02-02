import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

def remove_diacritics(text):
    # Normalize Alif variants to bare Alif
    text = re.sub(r'[أإآٱ]', 'ا', text)
    # Remove diacritics
    text = re.sub(r'[\u064B-\u065F\u0670\u0617-\u061A\u06D6-\u06ED]', '', text)
    # Remove Tatweel (elongation)
    text = re.sub(r'\u0640', '', text)
    return text

raw_text = '\u0628\u0650\u0633\u06e1\u0645\u0650 \u0671\u0644\u0644\u0651\u064e\u0647\u0650 \u0671\u0644\u0631\u0651\u064e\u062d\u06e1\u0645\u064e\u0670\u0646\u0650 \u0671\u0644\u0631\u0651\u064e\u062d\u0650\u064a\u0645\u0650'
cleaned = remove_diacritics(raw_text)
print(f"Original: {raw_text}")
print(f"Cleaned:  {cleaned}")
print(f"Hex:      {[hex(ord(c)) for c in cleaned]}")

expected_rahman = "الرحمن"
expected_rahim = "الرحيم"

if expected_rahman in cleaned:
    print("Found Al-Rahman")
else:
    print("NOT Found Al-Rahman")

if expected_rahim in cleaned:
    print("Found Al-Rahim")
else:
    print("NOT Found Al-Rahim")
