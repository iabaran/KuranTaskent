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
    text = text.replace('آ', 'ا') # Alif Madda -> Alif
    text = text.replace('إ', 'ا')
    text = text.replace('أ', 'ا')
    
    # Remove common Arabic diacritics + Tatweel
    text = re.sub(r'[\u064B-\u065F\u0617-\u061A\u06D6-\u06ED\u0640]', '', text)
    return text

def find_matches(target_forms, check_vowels=None):
    # target_forms: list of acceptable skeletons (without diacritics)
    # check_vowels: function(original_word) -> bool (optional extra check)
    
    occurrences = []
    
    for surah in data:
        for verse in surah['verses']:
            text = verse['text']
            clean_text = remove_diacritics(text)
            words = clean_text.split()
            original_words = text.split()
            
            for i in range(len(words)):
                word_clean = words[i]
                # Remove punctuation but keep letters
                w_skeleton = re.sub(r'[^\w\u0600-\u06FF]', '', word_clean)
                
                # Check if skeleton matches one of the targets
                if w_skeleton in target_forms:
                    match = True
                    
                    if check_vowels and i < len(original_words):
                        w_orig = original_words[i]
                        if not check_vowels(w_orig):
                            match = False
                    
                    if match:
                        occurrences.append({'s': surah['id'], 'a': verse['id']})
                        
    return occurrences

# 1. SATAN (Şeytan) 88
# Forms: شیطان (Singular), شياطين (Plural)
# Prefixes (Wa, Fa, Al, Li, Bi) might be attached?
# remove_diacritics doesn't remove prefixes.
# Skeleton check `w_skeleton in target_forms` requires EXACT match.
# But "Ash-Shaytan" -> Skeleton "alshytn"? 
# My previous script used partial match "starting with" or "containing"?
# "root in w_skeleton" was the previous logic.
# "alshytn" contains "shytn".
# But "shytnhm" (their devil)?
# Let's go back to partial match but with exclusions?
# Or generate all valid forms?
# Valid Satan forms in Quran:
# shaytan, al-shaytan, li-shaytan...
# It's safer to use "contains" but exclude known wrong endings?
# For Satan, "shytn" is quite unique.
# Let's use the robust "contains" logic but specific for Angel/Satan.

def find_matches_robust(root_pattern, logic_type="contains", exact_list=None, check_vowels=None):
    occurrences = []
    for surah in data:
        for verse in surah['verses']:
            text = verse['text']
            clean_text = remove_diacritics(text)
            words = clean_text.split()
            original_words = text.split()
            
            for i in range(len(words)):
                word_clean = words[i]
                w_skeleton = re.sub(r'[^\w\u0600-\u06FF]', '', word_clean)
                
                match = False
                
                if logic_type == "contains":
                    if root_pattern in w_skeleton:
                        match = True
                elif logic_type == "exact_list":
                    if w_skeleton in exact_list:
                        match = True
                
                if match and check_vowels and i < len(original_words):
                    if not check_vowels(original_words[i]):
                        match = False
                        
                if match:
                    occurrences.append({'s': surah['id'], 'a': verse['id']})
    return occurrences

# Satan Analysis
# "shytn" (Singular) and "shyATyn" (Plural)
# Contains logic works well for these as they are long distinct roots.
satan_locs = []
satan_locs.extend(find_matches_robust('شيطان'))
satan_locs.extend(find_matches_robust('شياطين'))
# Remove dups if any (though distinct roots)
# Sort
satan_locs.sort(key=lambda x: (x['s'], x['a']))


# Angel Analysis
# 1. Plural "Malaika" (mlAykt) -> Contains 'mlAykt' (normalized 'mlaykt'?)
# remove_diacritics normalizes Hamza to Alif?
# My function: text.replace('أ', 'ا') ...
# 'ملائكة' -> Hamza on Ya (\u0626). I didn't normalize that.
# So 'ملائكة' stays 'ملائكة' or just removing diacritics.
# Let's just search for 'ملائكة' in skeleton.
# Also need to handle 'Malaikatihi' where Ta Marbuta becomes Ta Maftuha (Open Ta)
# 'ملائكة' (Ta Marbuta) vs 'ملائكت' (Open Ta)
angel_plural = []
angel_plural.extend(find_matches_robust('ملائكة'))
angel_plural.extend(find_matches_robust('ملائكت'))

# Remove duplicates just in case (e.g. if I used 'mlAyk' it might match both, but separate is safer)
# robust search returns list of dicts.
# We should dedup based on s:a:word?
# find_matches_robust returns verse occurrences.
# If a verse has both? (Unlikely).
# If I search separately, I get list + list.
# I'll combine and dedup by s/a later.

# 2. Singular "Malak"
# Skeleton "mlk" is shared with King (Malik) and Possess (Malakat).
# We want strict skeletons:
# ملك (Malak/Malik), الملك (Al-Malak/Al-Malik), ملكا (Malakan), ملكين (Malakayn), الملكين (Al-Malakayn).
# Exclude: mlkt (Malakat), ymlk (Yamliku), etc.
mlk_skeletons = ['ملك', 'الملك', 'ملكا', 'ملكين', 'الملكين', 'بملك', 'للملك', 'wmlk'] 
# "wmlk" -> "wamalak"?
# Let's allow suffixes?
# Better to use "contains 'mlk'" BUT exclude if it ends with 't', 'n' (noon plural verb?), 'w' (plural verb)?
# "ymlkn" (yamlikun).
# "mlkt" (malakat).
# "mlkh" (mulkuhu).
# "mlkm" (mulkukum).
# EASIER: Check Vowels on the 'Lam'.
# Angel (Malak) -> Lam has Fatha.
# King (Malik) -> Lam has Kasra.
# Possess/Mulk -> Lam has Sukun (Mulk) or Kasra (Malik - King) or Fatha (Malaka - Verb).
# WAIT. "Malaka" (He possessed) has Fatha on Lam!
# But "Malaka" is a verb. Context?
# List of "Malak" vs "Malaka" locations?
# Usually "Malak" is noun. "Malaka" is verb "He possessed".
# "Malaka" appears? "Ma malakat" (She/What possessed - feminine/pl ref).
# "Malaka" (He possessed) -> Does it appear?
# Quran dictionary: Root M-L-K.
# "Malaka" (he possessed) occurs?
# "Amalak" (I possess)? "Amliku".
# Most verb forms have prefixes/suffixes.
# The form "Malak" (Meem-Lam-Kaf) with Fatha-Fatha as a whole word (with Al- or not) is Angel.
# The form "Malaka" (Verb) usually "Malakat".
# Is there "Malaka" (He possessed) without suffixes?
# 20:89 "La yamliku..."
# 4:3 ... ma malakat aymanukum.
# I will trust the "Lam Fatha" check + Exclusion of known verb skeletons like "mlkt".

def is_angel_vowel(w_orig):
    # Must have Lam + Fatha
    if not re.search(r'\u0644\u064E', w_orig):
        return False
    # Exclude if it looks like a verb "Malakat" (ends with t or matches mlkt in skeleton is handled by skeleton filter)
    # We will filter skeletons separately.
    return True

# Skeletons that ARE Angels (or Kings/Mulk before vowel check)
# Exclude 'mlkt', 'ymlk', 'nmlk', 'tmlk', 'mlkwt' (Mulkut), 'mlkh', 'mlkm'.
# We want to match 'ملك' inside the word, but the word must be a Noun.
# Nouns: Malak, Malik, Mulk.
# Verbs: Malaka, Yamliku...
# Acceptable Skeletons for Nouns:
# ملك, الملك, ملكا, الملك, لملك, بملك, والملك ... 
# Basically core 'mlk' with just prefixes (w, f, l, b, al) and suffixes (a, ani, yni - dual).
# NOT suffixes (t, tum, na, hu, hm, km).

valid_noun_skeletons = []
prefixes = ['', 'و', 'ف', 'ل', 'ب', 'ال', 'وال', 'فال', 'للملك']
cores = ['ملك', 'ملكا', 'ملكين'] # Singular, Accusative, Dual
# King 'Malik' is also 'ملك'.
# We will use check_vowels to distinguish Malak vs Malik.

for p in prefixes:
    for c in cores:
        valid_noun_skeletons.append(p + c)

# Add specific known ones if missed
# 'الملكين' (Al-Malakayn) -> Pref 'ال' + Core 'type?' -> 'ملكين' included.

angel_singular = find_matches_robust(None, logic_type="exact_list", exact_list=valid_noun_skeletons, check_vowels=is_angel_vowel)

angel_locs = angel_plural + angel_singular
# Do NOT dedup by s,a because some verses have multiple occurrences (e.g. 17:95)
angel_locs.sort(key=lambda x: (x['s'], x['a']))

print(f"Satan Count: {len(satan_locs)}")
print(f"Angel Count: {len(angel_locs)}")


# Write to JS file
js_content = f"""// Auto-generated by generate_angel_satan_js.py
// Satan Count: {len(satan_locs)}
const satanData = {json.dumps(satan_locs, indent=4)};

// Angel Count: {len(angel_locs)}
const angelData = {json.dumps(angel_locs, indent=4)};
"""

with open('angel_satan_data.js', 'w', encoding='utf-8') as f:
    f.write(js_content)
    
print("angel_satan_data.js created.")
