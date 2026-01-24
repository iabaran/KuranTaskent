import json
import sys

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

# Mukatta letters for each surah (Arabic letters)
MUKATTA_LETTERS = {
    2: ['ا', 'ل', 'م'],      # Alif Lam Mim
    3: ['ا', 'ل', 'م'],      # Alif Lam Mim
    7: ['ا', 'ل', 'م', 'ص'], # Alif Lam Mim Sad
    10: ['ا', 'ل', 'ر'],     # Alif Lam Ra
    11: ['ا', 'ل', 'ر'],     # Alif Lam Ra
    12: ['ا', 'ل', 'ر'],     # Alif Lam Ra
    13: ['ا', 'ل', 'م', 'ر'], # Alif Lam Mim Ra
    14: ['ا', 'ل', 'ر'],     # Alif Lam Ra
    15: ['ا', 'ل', 'ر'],     # Alif Lam Ra
    19: ['ك', 'ه', 'ي', 'ع', 'ص'], # Kaf Ha Ya Ain Sad
    20: ['ط', 'ه'],          # Ta Ha
    26: ['ط', 'س', 'م'],     # Ta Sin Mim
    27: ['ط', 'س'],          # Ta Sin
    28: ['ط', 'س', 'م'],     # Ta Sin Mim
    29: ['ا', 'ل', 'م'],     # Alif Lam Mim
    30: ['ا', 'ل', 'م'],     # Alif Lam Mim
    31: ['ا', 'ل', 'م'],     # Alif Lam Mim
    32: ['ا', 'ل', 'م'],     # Alif Lam Mim
    36: ['ي', 'س'],          # Ya Sin
    38: ['ص'],               # Sad
    40: ['ح', 'م'],          # Ha Mim
    41: ['ح', 'م'],          # Ha Mim
    42: ['ح', 'م'],          # Ha Mim (also has Ain Sin Qaf in verse 2)
    43: ['ح', 'م'],          # Ha Mim
    44: ['ح', 'م'],          # Ha Mim
    45: ['ح', 'م'],          # Ha Mim
    46: ['ح', 'م'],          # Ha Mim
    50: ['ق'],               # Qaf
    68: ['ن'],               # Nun
}

# Load Quran data
with open('quran_arabic.json', 'r', encoding='utf-8') as f:
    quran = json.load(f)

def clean_text(text):
    """Remove diacritics but keep consonants"""
    diacritics = ['ٰ', 'ْ', 'ٌ', 'ٍ', 'ً', 'ُ', 'ِ', 'َ', 'ّ', 'ٓ', 'ۚ', 'ۖ', 'ۗ', 'ۘ', 'ۙ', 'ۚ', 'ۛ', 'ۜ', '۟', '۠', 'ۡ', 'ۢ', 'ۣ', 'ۤ', 'ۥ', 'ۦ', 'ۧ', 'ۨ', '۩', '۪', '۫', '۬', 'ۭ', 'ۮ', 'ۯ', 'ٖ']
    for diacritic in diacritics:
        text = text.replace(diacritic, '')
    return text

def count_letters_in_surah(surah_id, letters):
    """Count specific letters in entire surah"""
    surah = next((s for s in quran if s['id'] == surah_id), None)
    if not surah:
        return None
    
    # Combine all verses into one text
    full_text = ' '.join([v['text'] for v in surah['verses']])
    clean = clean_text(full_text)
    
    counts = {}
    for letter in letters:
        # Also count Alef wasla (ٱ) as Alef (ا)
        if letter == 'ا':
            counts[letter] = clean.count('ا') + clean.count('ٱ')
        else:
            counts[letter] = clean.count(letter)
    
    return counts, len(surah['verses'])

print(f"{'Sure':<20} | {'No':<5} | {'Harfler':<20} | {'Harf Sayıları'}")
print("-" * 120)

for surah_id, letters in MUKATTA_LETTERS.items():
    surah = next((s for s in quran if s['id'] == surah_id), None)
    if surah:
        result = count_letters_in_surah(surah_id, letters)
        if result:
            counts, verse_count = result
            
            # Format letters
            letter_str = ' '.join(letters)
            
            # Format counts
            count_list = [f"{letter}: {counts[letter]}" for letter in letters]
            count_str = ', '.join(count_list)
            
            # Calculate total
            total = sum(counts.values())
            
            print(f"{surah['transliteration']:<20} | {surah_id:<5} | {letter_str:<20} | {count_str} | Toplam: {total}")

print("\n" + "="*120)
print("NOT: Alef (ا) sayımı, Alef Wasla (ٱ) karakterini de içerir.")
print("     Harekeler (şedde, cezm vb.) sayıma dahil değildir.")
