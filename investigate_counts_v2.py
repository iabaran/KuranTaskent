import json
import re
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def analyze_deeply():
    with open('quran_arabic.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    baqara = data[1] # Surah 2
    
    # Target values from user
    TARGET_WORDS = 6156
    TARGET_LETTERS = 26256

    # 1. Word Analysis
    base_split_words = 0
    waw_prefixes = 0
    li_prefixes = 0
    bi_prefixes = 0
    
    # 2. Letter Analysis
    core_letters = 0
    dagger_alifs = 0
    hamzas = 0
    shaddahs = 0
    
    # Character classes
    letter_pattern = re.compile(r'[\u0621-\u063A\u0641-\u064A\u0671-\u0680]')
    dagger_alif_char = '\u0670'
    shaddah_char = '\u0651'
    
    for v in baqara['verses']:
        text = v['text']
        words = text.split()
        base_split_words += len(words)
        
        for w in words:
            # Check prefixes (this is naive but let's see)
            # Waw prefix (and)
            if w.startswith('و') and len(w) > 1:
                waw_prefixes += 1
            # Li prefix (for)
            if w.startswith('ل') and len(w) > 1:
                li_prefixes += 1
            # Bi prefix (with)
            if w.startswith('ب') and len(w) > 1:
                bi_prefixes += 1
        
        core_letters += len(letter_pattern.findall(text))
        dagger_alifs += text.count(dagger_alif_char)
        shaddahs += text.count(shaddah_char)

    print(f"Base Words: {base_split_words}")
    print(f"Basmala Words: 4")
    print(f"Waw-prefixed words: {waw_prefixes}")
    print(f"Li-prefixed words: {li_prefixes}")
    print(f"Bi-prefixed words: {bi_prefixes}")
    
    total_w_v1 = base_split_words + 4
    print(f"Total Words (Base + Basmala): {total_w_v1}")
    print(f"Difference to 6156: {TARGET_WORDS - total_w_v1}")

    print(f"\nCore Letters: {core_letters}")
    print(f"Basmala Letters: 19")
    print(f"Dagger Alifs: {dagger_alifs}")
    print(f"Shaddahs: {shaddahs}")
    
    total_l_v1 = core_letters + 19
    print(f"Total Letters (Base + Basmala): {total_l_v1}")
    print(f"Difference to 26256: {TARGET_LETTERS - total_l_v1}")
    
    # Combining some marks
    print(f"Total Letters + Dagger Alifs: {total_l_v1 + dagger_alifs}")

if __name__ == "__main__":
    analyze_deeply()
