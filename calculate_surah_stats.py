import json
import re

EBCED_TABLE = {
    'ا': 1, 'ب': 2, 'ج': 3, 'د': 4, 'ه': 5, 'و': 6, 'ز': 7, 'ح': 8, 'ط': 9, 'ي': 10,
    'ك': 20, 'ل': 30, 'م': 40, 'ن': 50, 'س': 60, 'ع': 70, 'ف': 80, 'ص': 90, 'ق': 100,
    'ر': 200, 'ش': 300, 'ت': 400, 'ث': 500, 'خ': 600, 'ذ': 700, 'ض': 800, 'ظ': 900, 'غ': 1000,
    # Extra mappings for different script variants
    'ة': 5, 'ى': 10, 'ئ': 10, 'ؤ': 6, 'أ': 1, 'إ': 1, 'آ': 1, 'ء': 1, 'ٱ': 1
}

def normalize_for_ebced(text):
    # Remove diacritics but keep letters
    # We want to remove everything that is not one of the keys in EBCED_TABLE
    return text

def get_stats(surah_num):
    with open('quran_arabic.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    surah = next(s for s in data if s['id'] == surah_num)
    verses_stats = []
    total_ebced = 0
    total_chars_strict = 0
    total_chars_extended = 0
    total_words = 0

    for verse in surah['verses']:
        text = verse['text']
        
        # Word count
        words = text.split()
        total_words += len(words)

        # Harf count (strict)
        strict_text = re.sub(r'[^\u0621-\u063A\u0641-\u064A\u0671]', '', text)
        total_chars_strict += len(strict_text)

        # Harf count (extended - including Dagger Alif/Asar)
        extended_text = re.sub(r'[^\u0621-\u063A\u0641-\u064A\u0671\u0670]', '', text)
        total_chars_extended += len(extended_text)

        # Ebced
        clean_text = normalize_for_ebced(text)
        verse_ebced = sum(EBCED_TABLE.get(char, 0) for char in clean_text)
        total_ebced += verse_ebced

        verses_stats.append({
            "verse": verse['id'],
            "ebced": verse_ebced,
            "chars": len(strict_text)
        })

    return {
        "surah": surah_num,
        "total_ebced": total_ebced,
        "total_chars_strict": total_chars_strict,
        "total_chars_extended": total_chars_extended,
        "total_words": total_words,
        "verses": verses_stats
    }

def get_all_stats():
    with open('quran_arabic.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    all_stats = {}
    for surah in data:
        surah_num = surah['id']
        verses_stats = []
        total_ebced = 0
        total_chars_strict = 0
        total_chars_extended = 0
        total_words = 0

        for verse in surah['verses']:
            text = verse['text']
            words = text.split()
            total_words += len(words)
            strict_text = re.sub(r'[^\u0621-\u063A\u0641-\u064A\u0671]', '', text)
            total_chars_strict += len(strict_text)
            extended_text = re.sub(r'[^\u0621-\u063A\u0641-\u064A\u0671\u0670]', '', text)
            total_chars_extended += len(extended_text)
            clean_text = normalize_for_ebced(text)
            verse_ebced = sum(EBCED_TABLE.get(char, 0) for char in clean_text)
            total_ebced += verse_ebced
            verses_stats.append({
                "v": verse['id'],
                "e": verse_ebced,
                "c": len(strict_text)
            })

        all_stats[surah_num] = {
            "ebced": total_ebced,
            "chars_strict": total_chars_strict,
            "chars_extended": total_chars_extended,
            "words": total_words,
            "verses": verses_stats
        }
    return all_stats

all_surah_stats = get_all_stats()

js_content = f"const SURAH_STATS = {json.dumps(all_surah_stats, ensure_ascii=False)};"
with open('surah_stats.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print("All surah stats calculated and saved to surah_stats.js")
