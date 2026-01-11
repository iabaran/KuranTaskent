import json
import re
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def normalize_arabic(text):
    if not text: return ""
    # Remove all diacritics and signs
    noise = re.compile(r'[\u0610-\u061A\u064B-\u065F\u06D6-\u06ED\u08E4-\u08FE\u0670\u0671]')
    text = re.sub(noise, '', text)
    # Normalize Alef variants
    text = re.sub(r'[\u0622\u0623\u0625\u0671]', '\u0627', text)
    return text

EBCED_TABLE = {
    'ا': 1, 'ب': 2, 'ج': 3, 'د': 4, 'ه': 5, 'و': 6, 'ز': 7, 'ح': 8, 'ط': 9, 'ي': 10,
    'ك': 20, 'ل': 30, 'م': 40, 'ن': 50, 'س': 60, 'ع': 70, 'ف': 80, 'ص': 90, 'ق': 100,
    'ر': 200, 'ش': 300, 'ت': 400, 'ث': 500, 'خ': 600, 'ذ': 700, 'ض': 800, 'ظ': 900, 'غ': 1000
}

def analyze_baqara():
    with open('quran_arabic.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    baqara = data[1] # Surah 2
    
    alif = 'ا'
    lam = 'ل'
    mim = 'م'
    
    count_alif = 0
    count_lam = 0
    count_mim = 0
    total_words = 0
    
    for verse in baqara['verses']:
        norm = normalize_arabic(verse['text'])
        count_alif += norm.count(alif)
        count_lam += norm.count(lam)
        count_mim += norm.count(mim)
        # Word count per verse
        total_words += len(norm.split())

    total_alm = count_alif + count_lam + count_mim
    
    print(f"Surah Al-Baqara Analysis:")
    print(f"Alif Count: {count_alif}")
    print(f"Lam Count: {count_lam}")
    print(f"Mim Count: {count_mim}")
    print(f"Total A-L-M: {total_alm} (Divisible by 19: {total_alm % 19 == 0}, {total_alm}/19 = {total_alm/19:.2f})")
    print(f"Total Words: {total_words}")
    
    # Ebced of "Al-Baqarah" (البقرة)
    name = "البقرة"
    ebced_name = 0
    for char in name:
        if char == 'ة': ebced_name += 5
        elif char in EBCED_TABLE: ebced_name += EBCED_TABLE[char]
    
    print(f"Ebced value of 'Al-Baqarah' ({name}): {ebced_name}")

if __name__ == "__main__":
    analyze_baqara()
