import json
import re
import sys

# Example structure:
# [
#   { "id": "1", "name": "fatiha", "verses": [...] },
#   ...
# ]

def normalize_text(text):
    # Remove diacritics
    noise = re.compile(r'[\u0610-\u061A\u064B-\u065F\u06D6-\u06ED\u08E4-\u08FE\u0670\u0671]')
    return re.sub(noise, '', text)

def count_letters(text):
    # Core letters (Alif to Yeh) - following a standard approach
    # We include hamza variants.
    # Exclude spaces and diacritics.
    letters = re.findall(r'[\u0621-\u063A\u0641-\u064A\u0671]', text)
    return len(letters)

def main():
    try:
        with open('quran_arabic.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: quran_arabic.json not found")
        return

    fatiha = data[0]
    print(f"Surah: {fatiha['name']} (Surah 1)")
    
    total_raw_no_space = 0
    total_clean_letters = 0
    
    for i, verse in enumerate(fatiha['verses']):
        text = verse['text']
        clean = normalize_text(text)
        letters = count_letters(clean)
        
        words = text.split()
        
        print(f"Verse {i+1}:")
        print(f"  Words: {len(words)}")
        print(f"  Letters (clean): {letters}")
        print(f"  Content: {text}")
        
        total_clean_letters += letters
        total_raw_no_space += len(text.replace(' ', ''))

    print("-" * 20)
    print(f"Total Letters in Fatiha (clean): {total_clean_letters}")
    print(f"Total Chars (with diacritics, no spaces): {total_raw_no_space}")

if __name__ == "__main__":
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
    main()
