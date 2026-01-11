import json
import re
import sys

def count_strict_letters(text):
    # This pattern matches the 139-letter standard:
    # includes Alifs (all types), prevents diacritics
    # 0x0621-0x063A: Hamzas, Alifs, and letters up to Ghain
    # 0x0641-0x064A: Fa up to Yeh
    # 0x0671: Alif Wasla
    # EXCLUDES 0x0670 (Dagger Alif)
    letters = re.findall(r'[\u0621-\u063A\u0641-\u064A\u0671]', text)
    return len(letters), letters

def main():
    with open('quran_arabic.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    fatiha = data[0]
    
    total = 0
    print("Fatiha Verse-by-Verse Letter Count (Strict Script):")
    for i, verse in enumerate(fatiha['verses']):
        count, letters = count_strict_letters(verse['text'])
        total += count
        print(f"Verse {i+1}: {count} letters")
        # print(f"  Letters: {''.join(letters)}")
    
    print("-" * 30)
    print(f"Total: {total} letters")

if __name__ == "__main__":
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
    main()
