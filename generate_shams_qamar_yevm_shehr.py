#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Kur'an'da Şems (Güneş), Kamer (Ay), Şehr (Ay/Month), Yevm (Gün) kelimelerini arar
ve JS veri dosyası oluşturur.
"""

import json
import re

def normalize_arabic(text):
    """Remove diacritics for matching"""
    diacritics = re.compile(r'[\u064B-\u065F\u0670\u06D6-\u06ED\u0640]')
    return diacritics.sub('', text)

def load_quran():
    with open('quran_arabic.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def find_word_occurrences(quran, root_patterns):
    """Find all occurrences of words matching any pattern"""
    occurrences = []
    
    for surah in quran:
        surah_num = surah['id']
        for verse in surah.get('verses', []):
            verse_num = verse['id']
            text = verse['text']
            normalized_text = normalize_arabic(text)
            
            for pattern in root_patterns:
                normalized_pattern = normalize_arabic(pattern)
                if normalized_pattern in normalized_text:
                    occurrences.append({
                        's': surah_num,
                        'a': verse_num,
                        'w': pattern
                    })
                    break  # Count each verse only once
    
    return occurrences

def main():
    quran = load_quran()
    
    # Root patterns for each word
    # شمس - Shams (Sun)
    shams_patterns = ['شمس', 'الشمس']
    
    # قمر - Qamar (Moon) 
    qamar_patterns = ['قمر', 'القمر', 'والقمر']
    
    # شهر - Shehr (Month)
    shehr_patterns = ['شهر', 'الشهر', 'اشهر', 'الاشهر']
    
    # يوم - Yevm (Day) - tekil form only
    yevm_patterns = ['يوم', 'اليوم', 'يومئذ', 'يوما']
    
    shams_data = find_word_occurrences(quran, shams_patterns)
    qamar_data = find_word_occurrences(quran, qamar_patterns)
    shehr_data = find_word_occurrences(quran, shehr_patterns)
    yevm_data = find_word_occurrences(quran, yevm_patterns)
    
    print(f"Shams (Sun): {len(shams_data)} occurrences")
    print(f"Qamar (Moon): {len(qamar_data)} occurrences")
    print(f"Shehr (Month): {len(shehr_data)} occurrences")
    print(f"Yevm (Day): {len(yevm_data)} occurrences")
    
    # Create JS data file
    js_content = f"""// Shams (Sun) Data - {len(shams_data)} occurrences
const shamsData = {json.dumps(shams_data, ensure_ascii=False, indent=2)};

// Qamar (Moon) Data - {len(qamar_data)} occurrences
const qamarData = {json.dumps(qamar_data, ensure_ascii=False, indent=2)};

// Shehr (Month) Data - {len(shehr_data)} occurrences
const shehrData = {json.dumps(shehr_data, ensure_ascii=False, indent=2)};

// Yevm (Day) Data - {len(yevm_data)} occurrences
const yevmData = {json.dumps(yevm_data, ensure_ascii=False, indent=2)};
"""
    
    with open('shams_qamar_yevm_shehr_data.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print("\nData saved to shams_qamar_yevm_shehr_data.js")

if __name__ == '__main__':
    main()
