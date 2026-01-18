# -*- coding: utf-8 -*-
import json
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('quran_arabic.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def remove_diacritics(text):
    # Regex to remove Arabic diacritics
    text = re.sub(r'[\u064B-\u065F\u0670\u0617-\u061A\u06D6-\u06ED]', '', text)
    return text

print("--- ALLAH COUNT ANALYSIS ---")

allah_list = []
count_verses = 0
count_headers = 0

# 1. Count 'Allah' in all Verses (including Fatiha 1:1 and Naml 1:1 if present)
for surah in data:
    for verse in surah['verses']:
        clean_text = remove_diacritics(verse['text'])
        
        # Word-by-word analysis
        words = clean_text.split()
        verse_count = 0
        
        for w in words:
            w_clean = re.sub(r'[^\w\s]', '', w) # Remove punctuation
            
            # Match "Allah" (ٱللَّه) or "Lillah" (لِلَّهِ) or "Billah" (بِٱللَّهِ) etc.
            # Root: Alif-Lam-Lam-Ha (الله)
            # Variations:
            # الله (Allah)
            # بالله (Billah)
            # تالله (Tallahi)
            # لله (Lillahi)
            # فالله (Fallahu)
            # والله (Vallahi)
            # أالله (Aallahu)
            # اللهم (Allahumma) -> Counted or not? Usually Yes.
            
            # Simple check: Does it contain "الله" or "لله"?
            
            if 'الله' in w_clean or 'لله' in w_clean:
                # Check for "Allahumma" (اللهم)
                if 'اللهم' in w_clean:
                    # Is Allahumma counted in the 2698? Usually yes.
                    pass
                
                verse_count += 1
        
        if verse_count > 0:
            count_verses += verse_count
            for _ in range(verse_count):
                allah_list.append({'s': surah['id'], 'a': verse['id']})

print(f"Verse Count: {count_verses}")

# 2. Count "Allah" in Unnumbered Basmala Headers
# There are 114 Surahs.
# Surah 1 (Fatiha): Basmala is Verse 1. (Already counted above).
# Surah 9 (Tawbah): No Basmala.
# Rest (112 Surahs): Have unnumbered Basmala headers.
# Each Basmala contains "Allah" once ("Bismillah").

# Verify if Fatiha 1 is indeed in the json as a verse (It usually is).
# Let's assume yes based on previous work.

headers_list = []
header_count = 0

for s_id in range(1, 115):
    if s_id == 1: continue # Counted in verse
    if s_id == 9: continue # No Basmala
    
    # Add Header entry
    headers_list.append({'s': s_id, 'h': 1})
    header_count += 1

print(f"Header Count: {header_count}")

total_count = count_verses + header_count
print(f"Total Count: {total_count}")

# Generate JS if close to 2698
print("\nJS DATA GENERATION (Sample):")
# We will output this to a file or console later
