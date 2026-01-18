# -*- coding: utf-8 -*-
import json
import sys
import re

# Force UTF-8 stdout
sys.stdout.reconfigure(encoding='utf-8')

try:
    with open('quran_arabic.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    print("Error: quran_arabic.json not found.")
    sys.exit(1)

def remove_diacritics(text):
    # Normalize Alifs first
    text = text.replace('ٱ', 'ا') # Alif Wasla -> Alif
    text = text.replace('ٰ', 'ا') # Dagger Alif -> Alif
    text = text.replace('آ', 'ا') # Alif Madda -> Alif (simplify for search?) - Optional, maybe keep distinctive
    text = text.replace('إ', 'ا')
    text = text.replace('أ', 'ا')
    
    # Remove common Arabic diacritics (Tashkeel) + Tatweel (0640)
    # 064B-065F: Fathatan, Dammatan, Kasratan, Fatha, Damma, Kasra, Shadda, Sukun
    # 0670: Superscript Aleph (Already handled above, but if missed...)
    # 0617-061A: Small High corrections
    # 06D6-06ED: Quran annotations
    # 0640: Tatweel (Kashida)
    text = re.sub(r'[\u064B-\u065F\u0617-\u061A\u06D6-\u06ED\u0640]', '', text)
    return text

# Redirect output to file
results_file = open('results.txt', 'w', encoding='utf-8')
def log(msg):
    print(msg)
    try:
        results_file.write(msg + '\n')
    except:
        pass

def analyze_root_forms(root_pattern, display_name):
    log(f"\n======== ANALYZING: {display_name} ========")
    log(f"Searching for pattern: {root_pattern}")
    
    occurrences = []
    total_matches = 0
    form_counts = {}
    
    for surah in data:
        for verse in surah['verses']:
            # Use simple text without diacritics for search
            clean_text = remove_diacritics(verse['text'])
            
            words = clean_text.split()
            
            for word in words:
                # Remove punctuation attached to word (keep letters)
                word_clean = re.sub(r'[^\w\u0600-\u06FF]', '', word)
                
                if root_pattern in word_clean:
                    # Capture exact form
                    if word_clean not in form_counts:
                        form_counts[word_clean] = 0
                    form_counts[word_clean] += 1
                    total_matches += 1
                    occurrences.append(f"{surah['id']}:{verse['id']} - {word_clean}")

    log(f"Total Occurrences Found: {total_matches}")
    log("Forms Distribution:")
    sorted_forms = sorted(form_counts.items(), key=lambda x: x[1], reverse=True)
    for form, count in sorted_forms:
        log(f"  {form}: {count}")
        
    return total_matches, form_counts

# Debug: Check Surah 2 Verse 30 for Malaika
target_s = 2
target_v = 30
try:
    # ids are 1-based in json usually? or check file
    # data is list of surahs. surah['id'] == 1 is Fatiha usually.
    # index 1 is Surah 2 (Baqara).
    # verses list. index 29 is Verse 30.
    v_text = data[1]['verses'][29]['text']
    print(f"\n[DEBUG] Surah {target_s}:{target_v} Original: {v_text}")
    print(f"[DEBUG] Surah {target_s}:{target_v} Cleaned:  {remove_diacritics(v_text)}")
except Exception as e:
    print(f"[DEBUG] Error accessing 2:30: {e}")


# 1. SATAN (Şeytan)
# Singular: shaytan (شيطان)
# Plural: shayatin (شياطين)
analyze_root_forms('شيطان', 'SATAN (Singular: Shaytan)')
analyze_root_forms('شياطين', 'DEVILS (Plural: Shayatin)')

# 2. ANGEL (Melek)
# Singular: malak (ملك) 
# Note: 'malak' (king) also shares 'mlk'. 'Malak' (angel) is often 'malak'.
# Let's search for 'melek' forms specifically. 
# Usually "Malak" (Angel) is distinguished from "Malik" (King) by context or specific spelling in Uthmani script?
# In simple script 'ملك' matches both.
# But "Malaika" (Angels) is 'ملائكة'.

print("\n--- Note on ANGELS ---")
print("Searching specific forms primarily...")
analyze_root_forms('ملائكة', 'ANGELS (Plural: Malaika)')
analyze_root_forms('ملك', 'ANGEL/KING (Root: Malak/Malik)')


def analyze_exact_form_with_diacritics(pattern_regex, display_name):
    log(f"\n======== ANALYZING EXACT FORM: {display_name} ========")
    log(f"Searching for regex: {pattern_regex}")
    
    total_matches = 0
    
    for surah in data:
        for verse in surah['verses']:
            text = verse['text']
            # Regex findall
            # pattern should handle optional other diacritics if necessary, or be strict?
            # 'مَلَك' might be 'ٱلْمَلَكُ'
            # Letters: Meem (0645), Lam (0644), Kaf (0643)
            # Fatha: 064E
            # Pattern: \u0645\u064E\u0644\u064E\u0643
            # But wait, sometimes Fatha is omitted? Or there could be other marks?
            # Let's clean ONLY NON-FATHA/KASRA/DAMMA marks?
            # Or just search strict?
            
            matches = re.findall(pattern_regex, text)
            if matches:
                count = len(matches)
                total_matches += count
                # log(f"{surah['id']}:{verse['id']} - Found {count}")
                
    log(f"Total Exact Matches: {total_matches}")
    return total_matches

# Search for Malak (Angel) - Meem+Fatha+Lam+Fatha+Kaf
# Note: might be 'Malaka', 'Malaku', 'Malaki', 'Malakan'
# Regex: Meem, Fatha, Lam, Fatha, Kaf
# \u0645\u064E\u0644\u064E\u0643

# Remove detailed exact form calls to avoid regex errors, relying on categorize checks
# analyze_exact_form_with_diacritics(r'\u0645\u064E\u0644\u064E\u0643', 'Angel (Singular)')
# analyze_exact_form_with_diacritics(r'...', 'Angel (Dual)')

def categorize_mlk_matches():
    log("\n======== CATEGORIZING 'MLK' MATCHES ========")
    angel_count = 0
    king_count = 0
    mulk_count = 0
    other_count = 0
    
    # We re-scan 'mlk' matches
    root_pattern = 'ملك'
    
    for surah in data:
        for verse in surah['verses']:
            text = verse['text']
            # Clean for root check
            clean_text = remove_diacritics(text)
            words = clean_text.split()
            
            # Original words mapping?
            # We need to find the word in original text that corresponds to the match.
            # This is hard because splitting changes.
            # Let's iterate words in original text and check each.
            
            original_words = text.split()
            for w in original_words:
                w_clean = remove_diacritics(w)
                w_root = re.sub(r'[^\w\u0600-\u06FF]', '', w_clean)
                
                if root_pattern in w_root and 'ملائكة' not in w_root: # Exclude Malaika
                    # This word has 'mlk'. Analyze vowels on Lam.
                    # Find Lam \u0644
                    # Check next char.
                    # Normalized 'Lam' index in raw string is hard.
                    
                    # Regex on specific word w:
                    # Look for Lam followed by Fatha \u064E (Likely Angel)
                    # Look for Lam followed by Kasra \u0650 (Likely King)
                    # Look for Lam followed by Sukun \u0652 (Likely Mulk or Amliku)
                    
                    if re.search(r'\u0644\u064E', w): # Lam + Fatha
                        # Check previous char is Meem? 
                        if re.search(r'\u0645\u064E?\u0644\u064E', w) or re.search(r'\u0645\u0644\u064E', w):
                            # Meem (maybe Fatha) + Lam + Fatha
                            # Could be 'Malaka' (He possessed)? No 'Malaka' verb?
                            # 'Malaka' verb exists. "Ma Malakat aymanukum" (What your right hands possess).
                            # We need to distinguish NOMINAL "Malak" (Angel) from VERBAL "Malaka".
                            # "Malak" (Angel) usually noun.
                            
                            # Let's just log them to verify density.
                            # log(f"Candidate Angel: {w}")
                            angel_count += 1
                    elif re.search(r'\u0644\u0650', w): # Lam + Kasra
                         king_count += 1
                    elif re.search(r'\u0644\u0652', w): # Lam + Sukun
                         mulk_count += 1
                    else:
                         other_count += 1

    log(f"Potential Angels (Lam+Fatha): {angel_count}")
    log(f"Potential Kings (Lam+Kasra): {king_count}")
    return angel_count

categorize_mlk_matches()
