import json
import re
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def analyze_raw():
    with open('quran_arabic.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    baqara = data[1] # Surah 2
    
    # Let's count characters in different ways
    raw_chars = 0
    clean_chars = 0
    words_split = 0
    
    # Pattern for core Arabic letters (Alif to Yeh)
    # Includes Hamzas but not diacritics
    core_letters_pattern = re.compile(r'[\u0621-\u063A\u0641-\u064A\u0671-\u0680]')
    
    all_text = ""
    for verse in baqara['verses']:
        text = verse['text']
        all_text += " " + text
        raw_chars += len(text)
        
        # Word count by simple split
        words_split += len(text.split())
        
        # Letter count (only core letters, excluding marks)
        clean_chars += len(core_letters_pattern.findall(text))

    print(f"Baqara Stats (Internal Data):")
    print(f"Words (simple split): {words_split}")
    print(f"Raw Characters (inc spaces/marks): {raw_chars}")
    print(f"Clean Core Letters: {clean_chars}")
    
    # Let's see if we can identify common "missed" words
    # Like prefixes that should be words? No, Arabic is an agglutinative language.
    # But maybe the unnumbered Basmala?
    # Surah 1 has 7 verses, but Bakara is Surah 2.
    # Is the Basmala counted? 4 words.
    # 6118 + 4 = 6122. Still far from 6156.
    
    # 6156 - 6118 = 38 words.
    # Maybe some verses are split differently?
    
    # Let's print the first 3 verses and their counts according to my script
    print("\nFirst 3 Verses Analysis:")
    for i in range(3):
        v = baqara['verses'][i]
        txt = v['text']
        ws = len(txt.split())
        lc = len(core_letters_pattern.findall(txt))
        print(f"V{i+1}: {txt} (Words: {ws}, Letters: {lc})")

if __name__ == "__main__":
    analyze_raw()
