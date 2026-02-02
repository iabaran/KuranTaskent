import json
import re
import sys

# Set encoding for output
sys.stdout.reconfigure(encoding='utf-8')

def remove_diacritics(text):
    # Normalize Alif variants to bare Alif
    text = re.sub(r'[أإآٱ]', 'ا', text)
    # Remove diacritics
    text = re.sub(r'[\u064B-\u065F\u0670\u0617-\u061A\u06D6-\u06ED]', '', text)
    # Remove Tatweel (elongation)
    text = re.sub(r'\u0640', '', text)
    return text

def verify_counts():
    try:
        with open('quran_arabic.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: quran_arabic.json not found.")
        return

    ar_rahman_count = 0
    ar_rahman_locs = []
    
    ar_rahim_count = 0
    ar_rahim_locs = []
    
    ar_rahim_no_9_128_count = 0
    
    # Analyze verses
    for surah in data:
        surah_id = surah['id']
        for verse in surah['verses']:
            verse_id = verse['id']
            text = verse['text']
            clean_text = remove_diacritics(text)
            
            # Tokenize to avoid partial matches within other words (although with Al- these are specific)
            words = clean_text.split()
            
            # Count Ar-Rahman (الرحمن)
            # Note: We look for exact word match
            for word in words:
                if word == 'الرحمن':
                    ar_rahman_count += 1
                    ar_rahman_locs.append(f"{surah_id}:{verse_id}")
            
            # Count Ar-Rahim (الرحيم)
            for word in words:
                if word == 'الرحيم':
                    ar_rahim_count += 1
                    ar_rahim_locs.append(f"{surah_id}:{verse_id}")
                    
                    if not (surah_id == 9 and verse_id == 128):
                        ar_rahim_no_9_128_count += 1

    print(f"Total 'Ar-Rahman' (الرحمن) in verses: {ar_rahman_count}")
    print(f"Total 'Ar-Rahim' (الرحيم) in verses (ALL): {ar_rahim_count}")
    print(f"Total 'Ar-Rahim' (الرحيم) in verses (Excluding 9:128): {ar_rahim_no_9_128_count}")
    
    print("-" * 30)
    print("Verification:")
    if ar_rahman_count == 57:
        print("✅ Ar-Rahman count is exactly 57.")
    else:
        print(f"❌ Ar-Rahman count is {ar_rahman_count}, expected 57.")
        
    if ar_rahim_no_9_128_count == 114:
        print("✅ Ar-Rahim count (excluding 9:128) is exactly 114.")
    else:
        print(f"❌ Ar-Rahim count (excluding 9:128) is {ar_rahim_no_9_128_count}, expected 114.")

if __name__ == "__main__":
    verify_counts()
