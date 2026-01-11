import json
import re
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

EBCED_TABLE = {
    'ا': 1, 'ب': 2, 'ج': 3, 'د': 4, 'ه': 5, 'و': 6, 'ز': 7, 'ح': 8, 'ط': 9, 'ي': 10,
    'ك': 20, 'ل': 30, 'm': 40, 'ن': 50, 'س': 60, 'ع': 70, 'ف': 80, 'ص': 90, 'ق': 100,
    'ر': 200, 'ش': 300, 'ت': 400, 'ث': 500, 'خ': 600, 'ذ': 700, 'ض': 800, 'ظ': 900, 'غ': 1000,
    'ة': 5, 'ى': 10, 'ئ': 10, 'ؤ': 6, 'أ': 1, 'إ': 1, 'آ': 1, 'ء': 1
}

def normalize(text):
    noise = re.compile(r'[\u0610-\u061A\u064B-\u065F\u06D6-\u06ED\u08E4-\u08FE\u0670\u0671]')
    return re.sub(noise, '', text)

def get_ebced(text):
    text = normalize(text)
    total = 0
    for char in text:
        if char in EBCED_TABLE:
            total += EBCED_TABLE[char]
    return total

def fatiha_analysis():
    with open('quran_arabic.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    fatiha = data[0]
    
    total_ebced = 0
    word_details = []
    all_words = []
    
    for verse in fatiha['verses']:
        v_text = normalize(verse['text'])
        words = v_text.split()
        for w in words:
            e_val = get_ebced(w)
            total_ebced += e_val
            word_details.append((w, e_val))
            all_words.append(w)
            
    word_count = len(all_words)
    print(f"Sure: {fatiha['transliteration']}")
    print(f"Toplam Kelime Sayısı: {word_count}")
    print(f"Toplam Ebced Değeri: {total_ebced}")
    
    # Ebced ve 19 ilişkisi kontrolü
    if total_ebced % 19 == 0:
        print(f"Toplam Ebced 19'un katıdır: 19 * {total_ebced // 19}")
    
    print("\n--- Kelime Bazlı Ebced ---")
    for i, (w, v) in enumerate(word_details):
        print(f"{i+1}. {w}: {v}")

if __name__ == "__main__":
    fatiha_analysis()
