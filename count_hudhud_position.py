import json
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

def count_hudhud_position():
    try:
        with open('quran_arabic.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: quran_arabic.json not found.")
        return

    # Find Surah Neml (27)
    surah_neml = next((s for s in data if s['id'] == 27), None)
    if not surah_neml:
        print("Surah Neml not found!")
        return

    total_words_to_hudhud = 0
    hudhud_found = False
    
    # Target word
    target = "هدهد"

    print(f"--- NEML SURESİ (27) HÜTHÜT KELİME SAYIMI ---")

    for verse in surah_neml['verses']:
        if hudhud_found:
            break
            
        text = verse['text']
        # Simple splitting by whitespace
        words = text.split()
        
        for i, word in enumerate(words):
            # Clean word for comparison (remove some punctuation if attached, though simple split usually keeps diacritics)
            # We look for substring match because of attached prefixes/suffixes like 'wa', 'al', etc.
            # Normalization for check
            normalized_word = re.sub(r'[أإآٱ]', 'ا', word)
            normalized_word = re.sub(r'[\u064B-\u065F\u0670\u0617-\u061A\u06D6-\u06ED\u0640]', '', normalized_word)
            
            # Increment total before checking (1-indexed count)
            total_words_to_hudhud += 1
            
            if target in normalized_word:
                print(f"Hüthüt Bulundu!")
                print(f"Ayet: {verse['id']}")
                print(f"Kelime: {word} (Sıra: {total_words_to_hudhud})")
                print(f"Ayet İçi Sıra: {i + 1}")
                hudhud_found = True
                break

    if not hudhud_found:
        print("Hüthüt kelimesi bulunamadı (Normalization sorunu olabilir).")

if __name__ == "__main__":
    count_hudhud_position()
