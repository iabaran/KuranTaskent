import json

# Known Mukatta Surah IDs
MUKATTA_SURAHS = [
    2, 3, 7, 
    10, 11, 12, 13, 14, 15, 
    19, 20, 
    26, 27, 28, 
    29, 30, 31, 32, 
    36, 38, 
    40, 41, 42, 43, 44, 45, 46, 
    50, 68
]

with open('quran_arabic.json', 'r', encoding='utf-8') as f:
    quran = json.load(f)

import sys

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

print(f"{'Sure':<20} | {'No':<5} | {'Ayet':<30} | {'Harf Sayıları'}")
print("-" * 120)

for surah_id in MUKATTA_SURAHS:
    surah = next((s for s in quran if s['id'] == surah_id), None)
    if surah:
        first_verse = surah['verses'][0]['text']
        
        # Normalize: Remove typical diacritics to engage with raw letters
        # Keeping it simple: just count the letters present in the verse
        # Usually looking for: Alif, Lam, Mim, Sad, Ra, Kaf, Ha, Ya, Ain, Qaf, Nun
        
        # Clean but keep letters
        clean_chars = [c for c in first_verse if c not in [' ', 'ٰ', 'ْ', 'ٌ', 'ٍ', 'ً', 'ُ', 'ِ', 'َ', 'ّ', 'ٓ', 'ٱ', ' ']]
        
        # Unique letters in this mukatta (preserves order roughly)
        unique_letters = []
        for c in clean_chars:
            if c not in unique_letters:
                unique_letters.append(c)
                
        counts = []
        for letter in unique_letters:
            count = clean_chars.count(letter)
            counts.append(f"{letter}: {count}")
            
        count_str = ", ".join(counts)
        print(f"{surah['transliteration']:<20} | {surah['id']:<5} | {first_verse:<30} | {count_str}")

