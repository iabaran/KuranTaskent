import json
import sys

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

# Mukatta letters for each surah
MUKATTA_LETTERS = {
    2: ['ا', 'ل', 'م'],      # Alif Lam Mim
    3: ['ا', 'ل', 'م'],      
    7: ['ا', 'ل', 'م', 'ص'], 
    10: ['ا', 'ل', 'ر'],     
    11: ['ا', 'ل', 'ر'],     
    12: ['ا', 'ل', 'ر'],     
    13: ['ا', 'ل', 'م', 'ر'], 
    14: ['ا', 'ل', 'ر'],     
    15: ['ا', 'ل', 'ر'],     
    19: ['ك', 'ه', 'ي', 'ع', 'ص'], 
    20: ['ط', 'ه'],          
    26: ['ط', 'س', 'م'],     
    27: ['ط', 'س'],          
    28: ['ط', 'س', 'م'],     
    29: ['ا', 'ل', 'م'],     
    30: ['ا', 'ل', 'م'],     
    31: ['ا', 'ل', 'م'],     
    32: ['ا', 'ل', 'م'],     
    36: ['ي', 'س'],          
    38: ['ص'],               
    40: ['ح', 'م'],          
    41: ['ح', 'م'],          
    42: ['ح', 'م'],          
    43: ['ح', 'م'],          
    44: ['ح', 'م'],          
    45: ['ح', 'م'],          
    46: ['ح', 'م'],          
    50: ['ق'],               
    68: ['ن'],               
}

# Basmala text
BASMALA = "بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ"

# Load Quran data
with open('quran_arabic.json', 'r', encoding='utf-8') as f:
    quran = json.load(f)

def clean_text(text):
    """Remove diacritics but keep consonants"""
    diacritics = ['ٰ', 'ْ', 'ٌ', 'ٍ', 'ً', 'ُ', 'ِ', 'َ', 'ّ', 'ٓ', 'ۚ', 'ۖ', 'ۗ', 'ۘ', 'ۙ', 'ۚ', 'ۛ', 'ۜ', '۟', '۠', 'ۡ', 'ۢ', 'ۣ', 'ۤ', 'ۥ', 'ۦ', 'ۧ', 'ۨ', '۩', '۪', '۫', '۬', 'ۭ', 'ۮ', 'ۯ', 'ٖ']
    for diacritic in diacritics:
        text = text.replace(diacritic, '')
    return text

def count_letter(text, letter):
    """Count letter with Alef variants"""
    if letter == 'ا':
        return text.count('ا') + text.count('ٱ')
    else:
        return text.count(letter)

def analyze_surah_comprehensive(surah_id, letters):
    """Comprehensive letter count including Basmala and first verse"""
    surah = next((s for s in quran if s['id'] == surah_id), None)
    if not surah:
        return None
    
    # Count in Basmala (for non-Fatiha, non-Tawbah)
    basmala_counts = {}
    if surah_id != 1 and surah_id != 9:  # Not Fatiha, not Tawbah
        clean_basmala = clean_text(BASMALA)
        for letter in letters:
            basmala_counts[letter] = count_letter(clean_basmala, letter)
    else:
        for letter in letters:
            basmala_counts[letter] = 0
    
    # Count in first verse (Mukatta itself)
    first_verse = surah['verses'][0]['text']
    clean_first = clean_text(first_verse)
    first_verse_counts = {}
    for letter in letters:
        first_verse_counts[letter] = count_letter(clean_first, letter)
    
    # Count in entire surah
    full_text = ' '.join([v['text'] for v in surah['verses']])
    clean_full = clean_text(full_text)
    total_counts = {}
    for letter in letters:
        total_counts[letter] = count_letter(clean_full, letter)
    
    # Grand total = Basmala + Total in surah
    grand_total = {}
    for letter in letters:
        grand_total[letter] = basmala_counts[letter] + total_counts[letter]
    
    return {
        'basmala': basmala_counts,
        'first_verse': first_verse_counts,
        'surah_total': total_counts,
        'grand_total': grand_total
    }

print("=" * 140)
print("HARFLERLE BAŞLAYAN SURERİN KOMPREHANSİF ANALİZİ")
print("=" * 140)
print()

for surah_id, letters in MUKATTA_LETTERS.items():
    surah = next((s for s in quran if s['id'] == surah_id), None)
    if not surah:
        continue
    
    result = analyze_surah_comprehensive(surah_id, letters)
    if not result:
        continue
    
    print(f"📖 {surah['transliteration']} Suresi (No: {surah_id})")
    print(f"   Harfler: {' '.join(letters)}")
    print()
    
    # Basmala counts
    if surah_id != 1 and surah_id != 9:
        basmala_str = ', '.join([f"{l}: {result['basmala'][l]}" for l in letters])
        basmala_sum = sum(result['basmala'].values())
        print(f"   🕌 Besmele'de: {basmala_str} (Toplam: {basmala_sum})")
    else:
        if surah_id == 1:
            print(f"   🕌 Besmele: Fatiha'da başlangıç olarak sayılır")
        else:
            print(f"   🕌 Besmele: Tevbe suresinde besmele yok")
    
    # First verse (Mukatta) counts
    first_str = ', '.join([f"{l}: {result['first_verse'][l]}" for l in letters])
    first_sum = sum(result['first_verse'].values())
    print(f"   📜 1. Ayet (Mukatta): {first_str} (Toplam: {first_sum})")
    
    # Surah total
    surah_str = ', '.join([f"{l}: {result['surah_total'][l]}" for l in letters])
    surah_sum = sum(result['surah_total'].values())
    print(f"   📊 Sure İçinde Toplam: {surah_str} (Toplam: {surah_sum})")
    
    # Grand total
    grand_str = ', '.join([f"{l}: {result['grand_total'][l]}" for l in letters])
    grand_sum = sum(result['grand_total'].values())
    print(f"   ✅ GENEL TOPLAM (Besmele + Sure): {grand_str} (Toplam: {grand_sum})")
    
    # Check if divisible by 19
    if grand_sum % 19 == 0:
        print(f"   🌟 19'a Bölünebilir: {grand_sum} = 19 × {grand_sum // 19}")
    
    print()

print("=" * 140)
print("NOT: Alef (ا) sayımı, Alef Wasla (ٱ) karakterini de içerir.")
print("     Harekeler sayıma dahil değildir.")
print("=" * 140)
