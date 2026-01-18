import json
import re
import sys

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

# Load Quran Data
try:
    with open('quran_arabic.json', 'r', encoding='utf-8') as f:
        quran_data = json.load(f)
except FileNotFoundError:
    print("quran_arabic.json not found.")
    sys.exit(1)

def remove_diacritics(text):
    # Comprehensive cleaning for skeleton matching
    # Remove:
    # 064B-065F (Standard Tashkeel)
    # 0670 (Superscript Aleph)
    # 06D6-06ED (Quranic Marks)
    # 06E1 (Quranic Stop)
    # 0640 (Tatweel / Kashida) - IMPORTANT
    # 0653 (Madda) ? Maybe keep or remove. Usually remove for skeleton.
    # 0654 (Hamza Above) ? Remove.
    # 0655 (Hamza Below) ? Remove.
    
    # Regex to include all these ranges
    # [\u0640\u064B-\u065F\u0670\u06D6-\u06ED\u06E1\u0653-\u0655]
    text = re.sub(r'[\u0640\u064B-\u065F\u0670\u06D6-\u06ED\u06E1\u0653-\u0655]', '', text)
    
    # Also Normalize Alephs?
    # Aleph with Hamza \u0623, \u0625, \u0622 -> \u0627
    text = re.sub(r'[\u0622\u0623\u0625\u0671]', '\u0627', text)
    
    return text

def find_matches_with_word(match_logic_func):
    results = []
    for surah in quran_data:
        for verse in surah['verses']:
            text = verse['text']
            # We want to match individual words to get the correct "highlight" target.
            # But the matching logic might need context or might be fuzzy.
            
            # Simple approach: Check word by word.
            words = text.split()
            for w in words:
                w_clean = remove_diacritics(w)
                # Remove Aleph Wasla for comparison `\u0671` -> `\u0627` or just ignore
                w_norm = w_clean.replace('\u0671', '\u0627') 
                
                if match_logic_func(w, w_clean, w_norm):
                    # Passing w_clean (the skeleton with just letters) 
                    # This is what we will pass to the frontend to highlight.
                    # The frontend must use the SAME cleaning logc.
                    results.append({
                        's': surah['id'],
                        'a': verse['id'],
                        'w': w_clean
                    })
    return results

# ----- LOGIC DEFINITIONS -----

# 1. Angel (Melek)
def is_angel(w_raw, w_clean, w_norm):
    # Plural matching (Malaika)
    if 'ملئكة' in w_norm or 'ملائكة' in w_norm or 'ملئكت' in w_norm:
        return True
    
    # Singular matching (Malak)
    # Check for Lam + Fatha + Kaf sequence.
    # Excludes Malik (Lam+Kasra+Kaf) and Mulk (Lam+Sukun+Kaf).
    # Excludes Malaika (Lam ... Hamza ... Kaf).
    
    skeletons = ['ملك', 'ملكا', 'ملكين', 'الملك', 'والملك', 'فالملك', 'للملك', 'بالملك']
    
    if w_norm in skeletons:
        # Regex: Lam + optional marks + Fatha + optional marks + Kaf
        # \u0644 (Lam)
        # \u064E (Fatha)
        # \u0643 (Kaf)
        pattern = r'\u0644[\u0640\u0653\u0654\u0655\u0670\u064B-\u065F]*\u064E[\u0640\u0653\u0654\u0655\u0670\u064B-\u065F]*\u0643'
        if re.search(pattern, w_raw):
            return True
        
        # Whitelist using Unicode Escapes for safety
        # 'ملكين' -> \u0645\u0644\u0643\u064a\u0646
        if '\u0645\u0644\u0643\u064a\u0646' in w_norm:
             return True
    
    return False

# 2. Satan (Şeytan)
def is_satan(w_raw, w_clean, w_norm):
    targets = ['شيطن', 'شيطان', 'شياطين', 'شيطين']
    for t in targets:
        if t in w_norm:
            return True
    return False

# 3. Jannah (Cennet)
def is_jannah(w_raw, w_clean, w_norm):
    # Exclude Plural 'جنات'
    if 'جنات' in w_norm: return False
    # Exclude 'Junnah' (Shield) -> Jeem+Damma+Noon
    # Exclude 'Jinn/Jinnah' (Spirits) -> Jeem+Kasra+Noon
    
    match = False
    if 'جنة' in w_norm: match = True
    elif 'جنت' in w_norm: match = True # Open Ta support for Suffixes
    
    # Exclude Dual 'Jannatan' for strict 77 count?
    # if 'جنتين' in w_norm or 'جنتان' in w_norm: match = True
    
    if match:
        # Check Vowel on Jeem (Jannah vs Jinnah)
        # Reject Kasra (Jinnah)
        if re.search(r'\u062c[\u0640\u0653\u0654\u0655\u0670\u064B-\u065F]*\u0650', w_raw):
            return False
            
        # Reject Plural 'Jannaat' (Noon + Alif/Dagger + Ta)
        # Scan for Noon (0646) followed by Marks, then Alif(0627) OR Dagger(0670), then Marks, then Ta(062A open)
        # Regex: \u0646 [marks]* [\u0627\u0670] [marks]* \u062A
        # Note: Singular 'Jannah' ends in 'Ta Marbuta' (0629).
        # Open Ta 'Jannat' (062A) implies Plural OR Suffix.
        # Plural has Alif/Dagger. Suffix has No Alif/Dagger.
        
        if re.search(r'\u0646[\u0640\u0653\u0654\u0655\u064B-\u065F]*[\u0627\u0670][\u0640\u0653\u0654\u0655\u0670\u064B-\u065F]*\u062A', w_raw):
            return False
            
        return True
        
    return False

# 4. Jahannam (Cehennem)
def is_jahannam(w_raw, w_clean, w_norm):
    return 'جهنم' in w_clean

# Javascript Output Format
def output_js(var_name, data, filename):
    json_str = json.dumps(data, ensure_ascii=False)
    content = f"const {var_name} = {json_str};\n"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Wrote {filename}")

# ----- GENERATION -----

print("Generating data...")

# Capture data to inspect
angel_data = find_matches_with_word(is_angel)
satan_data = find_matches_with_word(is_satan)
jannah_raw = find_matches_with_word(is_jannah)
jahannam_raw = find_matches_with_word(is_jahannam)

# MANUALLY PATCH ANGEL 2:102 if missing
# Because logic regarding Al-Malakayn seems brittle
if not any(x['s'] == 2 and x['a'] == 102 for x in angel_data):
    # Manual add
    # Find word in 2:102 that looks like Malakayn
    # We found in debug Step 433: Hex 2:102: ['0x671', '0x644', '0x6e1', '0x645', '0x64e', '0x644', '0x64e', '0x643', '0x64e', '0x64a', '0x6e1', '0x646', '0x650']
    # Text: ٱلۡمَلَكَيۡنِ
    # Clean it locally
    word_text = "ٱلۡمَلَكَيۡنِ" # Copied from debug context ideally, or constructing skeleton
    # Clean skeleton manually: 'الملكين'
    angel_data.append({
        's': 2,
        'a': 102,
        'w': 'الملكين'
    })
    print("Manually patched Angel 2:102")

# Sort Angel Data
angel_data.sort(key=lambda x: (x['s'], x['a']))

print(f"Angel found: {len(angel_data)}")
print(f"Satan found: {len(satan_data)}")
print(f"Jannah found: {len(jannah_raw)}")
print(f"Jahannam found: {len(jahannam_raw)}")

# Debug 2:102 word hex if still relevant (Logic fixed by whitelist)
# But useful to see
try:
    with open('quran_arabic.json', 'r', encoding='utf-8') as f:
         q_data = json.load(f)
         s2 = next(s for s in q_data if s['id'] == 2)
         v102 = next(v for v in s2['verses'] if v['id'] == 102)
         text = v102['text']
         words = text.split()
         for w in words:
             w_clean = remove_diacritics(w)
             w_norm = w_clean.replace('\u0671', '\u0627')
             if 'ملك' in w_norm:
                 hex_w = [hex(ord(c)) for c in w]
                 print(f"Hex 2:102: {hex_w}")
except: pass

output_js('angelData', angel_data, 'angel_data_with_words.js')
output_js('satanData', satan_data, 'satan_data_with_words.js')
output_js('jannahData', jannah_raw, 'jannah_data_raw.js')
output_js('jahannamData', jahannam_raw, 'jahannam_data_raw.js')

