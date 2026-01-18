# -*- coding: utf-8 -*-
import json
import sys
import re

# Force UTF-8 for stdout
sys.stdout.reconfigure(encoding='utf-8')

with open('quran_arabic.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def remove_diacritics(text):
    # Remove standard diacritics
    text = re.sub(r'[\u064B-\u065F\u0670\u0617-\u061A\u06D6-\u06ED]', '', text)
    return text

def analyze_word_variants(root, display_name):
    print(f"\nANALYZING: {display_name} (Root: {root})")
    
    variants = {}
    total = 0
    
    for surah in data:
        for verse in surah['verses']:
            clean = remove_diacritics(verse['text'])
            words = clean.split()
            
            for w in words:
                if root in w:
                    # Clean punctuation from word for better grouping
                    # remove non-letter chars at start/end
                    w_clean = re.sub(r'[^\w\s]', '', w) 
                    
                    if w not in variants:
                        variants[w] = 0
                    variants[w] += 1
                    total += 1

    print(f"Total Occurrences containing root: {total}")
    print("Top Word Forms Found:")
    
    sorted_vars = sorted(variants.items(), key=lambda x: x[1], reverse=True)
    for w, c in sorted_vars[:200]:
        print(f"  {w}: {c}")
        
    return sorted_vars

# Analyze Yevm (Day) - يوم
# Target: 365 (Singular)
# Common forms: yevm, yevmen, el-yevm
# Exclude: yevmeyni (2), eyyam (plural)
print("--- DAY ---")
yevm_vars = analyze_word_variants('يوم', 'Day (Yevm)')

# Analyze Shehr (Month) - شهر
# Target: 12 (Singular)
# Common forms: shahr, al-shahr
# Exclude: ashhur (months), shahrayn (2 months)
print("\n--- MONTH ---")
shehr_vars = analyze_word_variants('شهر', 'Month (Shehr)')

# Need to manually construct the list of "Singular" words based on output
# Common valid singulars for Yevm: 
# يوم (yevm)
# يوما (yevman)
# اليوم (al-yevm)
# بيوم (bi-yevm)
# ليوم (li-yevm)
# فاليوم (fal-yevm)
# واليوم (wal-yevm)
# يومهم (yevmihim - with suffix? usually suffix forms are excluded in simple counts, but let's see)
# 
# Plurals/Duals to exclude:
# يومين (yevmayn - 2 days)
# ايام (ayyam - days) - Root is different (y-w-m vs a-y-m?) No, plural of yevm is ayyam.
# But 'ayyam' doesn't contain 'يوم' string usually (contains ي a m).
# Ah, 'يوم' string search might miss plurals like 'ayyam' (ايام). That's GOOD.
# We only want singular.
# 
# Wait, 'yevmayn' (يومين) contains 'yevm'.
# 'yevmeizin' (يومئذ) ? (That day). usually counted separate?
