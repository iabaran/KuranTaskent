# -*- coding: utf-8 -*-
import json
import sys
import re

# Force UTF-8 stdout
sys.stdout.reconfigure(encoding='utf-8')

with open('quran_arabic.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def remove_diacritics(text):
    text = re.sub(r'[\u064B-\u065F\u0670\u0617-\u061A\u06D6-\u06ED]', '', text)
    return text

def analyze_word(root, display_name):
    print(f"\nANALYZING: {display_name} (Root: {root})")
    
    occurrences = []
    total_count = 0
    
    for surah in data:
        for verse in surah['verses']:
            clean = remove_diacritics(verse['text'])
            # Simple string search first to catch all forms
            if root in clean:
                # Count exact matches of the root string
                # Note: 'jannah' (جنة) might be part of 'jannat' (جنات plural)
                # Usually the count equality refers to Singular/Specific forms or ANY form?
                # Let's count totals first and see what we get.
                # Commonly cited miracle: "Seven Heavens" 7 times, etc.
                # Jannah 77, Jahannam 77.
                
                # Check for word boundary issues later if needed.
                matches = clean.count(root)
                if matches > 0:
                    for _ in range(matches):
                        occurrences.append({'s': surah['id'], 'a': verse['id'], 'text': verse['text']})
                    total_count += matches

    print(f"Total Raw Occurrences: {total_count}")
    return occurrences

# Analyze Jannah (Paradise)
# Root often: جنة (singular) or جنات (plural). The miracle usually cites "Jannah" (singular).
# Let's check Singular 'جنة'
print("--- JANNAH ---")
jannah_raw = analyze_word('جنة', 'Jannah (Paradise)')

# Analyze Jahannam (Hell)
# Root: جهنم
print("\n--- JAHANNAM ---")
jahannam_raw = analyze_word('جهنم', 'Jahannam (Hell)')

# Let's print unique singular forms to refine
def refine_analysis(locations, target_root):
    exact_forms = {}
    valid_locs = []
    
    for item in locations:
        clean = remove_diacritics(item['text'])
        words = clean.split()
        for w in words:
            # remove punctuation
            w_clean = re.sub(r'[^\w\s]', '', w)
            if target_root in w_clean:
                # Check if it is really the word we want
                if w_clean not in exact_forms:
                    exact_forms[w_clean] = 0
                exact_forms[w_clean] += 1
                
                # Filter specifically:
                # For Jannah: we want Singular "Jannah" (جنة) specifically? 
                # Or total?
                # If target is 77, let's see which forms sum to 77.
                pass

    print("\nWord Forms Found:")
    for w, c in sorted(exact_forms.items(), key=lambda x: x[1], reverse=True):
        print(f"  {w}: {c}")

refine_analysis(jannah_raw, 'جنة')
refine_analysis(jahannam_raw, 'جهنم')
