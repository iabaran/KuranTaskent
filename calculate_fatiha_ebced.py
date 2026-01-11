import json
import re
import sys

# Standard Ebced Table
EBCED_TABLE = {
    'ا': 1, 'ب': 2, 'ج': 3, 'د': 4, 'ه': 5, 'و': 6, 'ز': 7, 'ح': 8, 'ط': 9, 'ي': 10,
    'ك': 20, 'ل': 30, 'م': 40, 'ن': 50, 'س': 60, 'ع': 70, 'ف': 80, 'ص': 90, 'ق': 100,
    'ر': 200, 'ش': 300, 'ت': 400, 'ث': 500, 'خ': 600, 'ذ': 700, 'ض': 800, 'ظ': 900, 'غ': 1000,
    # Specials and variants
    'ة': 5,   # Ta Marbuta -> 5 (counted as H)
    'ى': 10,  # Alif Maqsura -> 10 (counted as Y)
    'ئ': 10,  # Ya with Hamza -> 10 (carrier is Y)
    'ؤ': 6,   # Waw with Hamza -> 6 (carrier is W)
    'أ': 1,   # Alif with Hamza -> 1 (carrier is A)
    'إ': 1,   # Alif with Hamza -> 1 (carrier is A)
    'آ': 1,   # Alif Madda -> 1
    'ء': 1,   # Isolated Hamza -> 1
    'ٱ': 1,   # Alif Wasla -> 1
}

def normalize_for_ebced(text):
    # Remove diacritics and non-letter marks (including Shadda, Sukun, etc.)
    # We keep the core letters.
    # Pattern for core letters: [\u0621-\u063A\u0641-\u064A\u0671]
    # Plus Dagger Alif (0x0670) which is sometimes counted as 1, but usually NOT in strict letter-based Ebced.
    # Most Ebced calculations are based on the written script (Resm-i Osmani).
    
    # Let's count characters that ARE in the Ebced table.
    return text

def calculate_ebced(text):
    total = 0
    breakdown = []
    for char in text:
        if char in EBCED_TABLE:
            val = EBCED_TABLE[char]
            total += val
            breakdown.append((char, val))
    return total, breakdown

def main():
    try:
        with open('quran_arabic.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: quran_arabic.json not found")
        return

    fatiha = data[0]
    grand_total = 0
    
    print(f"Ebced Analysis for {fatiha['name']} (Surah 1):")
    print("-" * 40)
    
    for i, verse in enumerate(fatiha['verses']):
        v_ebced, v_breakdown = calculate_ebced(verse['text'])
        grand_total += v_ebced
        print(f"Verse {i+1}: {v_ebced}")
        # print(f"  Letters: {' '.join([f'{c}({v})' for c, v in v_breakdown])}")

    print("-" * 40)
    print(f"Total Ebced Value of Fatiha: {grand_total}")
    
    # Common Fatiha Ebced value in literature is often cited as 10143 or similar depending on specifics.
    # Let's see what our calculation gives.

if __name__ == "__main__":
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
    main()
