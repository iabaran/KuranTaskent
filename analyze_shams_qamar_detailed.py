#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Kur'an'da Şems (Güneş) ve Kamer (Ay) kelimelerini detaylı olarak arar.
"""

import json
import re
import sys

# Encoding fix for Windows
sys.stdout.reconfigure(encoding='utf-8')

def load_quran():
    with open('quran_arabic.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def normalize_arabic(text):
    """Remove all diacritics for matching"""
    diacritics = re.compile(r'[\u064B-\u065F\u0670\u06D6-\u06ED\u0640\u0653-\u0655]')
    return diacritics.sub('', text)

def find_all_forms(quran, root, name):
    """Find all forms of a word and list them with verse references"""
    occurrences = []
    forms_found = {}
    
    normalized_root = normalize_arabic(root)
    
    for surah in quran:
        surah_num = surah['id']
        
        for verse in surah.get('verses', []):
            verse_num = verse['id']
            text = verse['text']
            normalized_text = normalize_arabic(text)
            
            # Check if root exists in normalized text
            if normalized_root in normalized_text:
                # Find the actual word form
                words = text.split()
                for word in words:
                    normalized_word = normalize_arabic(word)
                    if normalized_root in normalized_word:
                        occurrences.append({
                            's': surah_num,
                            'a': verse_num,
                            'w': word
                        })
                        
                        # Track different forms
                        clean_word = normalize_arabic(word)
                        if clean_word not in forms_found:
                            forms_found[clean_word] = []
                        forms_found[clean_word].append(f"{surah_num}:{verse_num}")
                        break  # Count each verse only once
    
    return occurrences, forms_found

def main():
    quran = load_quran()
    
    # Şems (شمس) - Sun
    shams_data, shams_forms = find_all_forms(quran, 'شمس', 'Gunes')
    
    # Kamer (قمر) - Moon  
    qamar_data, qamar_forms = find_all_forms(quran, 'قمر', 'Kamer')
    
    # Write results to file
    with open('shams_qamar_analysis.txt', 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write(f"Güneş (Şems) شمس - Toplam: {len(shams_data)} ayet\n")
        f.write("=" * 60 + "\n")
        
        f.write(f"\nBulunan formlar ({len(shams_forms)} farklı form):\n")
        for form, verses in sorted(shams_forms.items(), key=lambda x: -len(x[1])):
            f.write(f"  {form}: {len(verses)} kez\n")
        
        f.write(f"\nTüm ayetler:\n")
        for i, occ in enumerate(shams_data, 1):
            f.write(f"  {i}. {occ['s']}:{occ['a']} - {occ['w']}\n")
        
        f.write("\n\n" + "=" * 60 + "\n")
        f.write(f"Ay (Kamer) قمر - Toplam: {len(qamar_data)} ayet\n")
        f.write("=" * 60 + "\n")
        
        f.write(f"\nBulunan formlar ({len(qamar_forms)} farklı form):\n")
        for form, verses in sorted(qamar_forms.items(), key=lambda x: -len(x[1])):
            f.write(f"  {form}: {len(verses)} kez\n")
        
        f.write(f"\nTüm ayetler:\n")
        for i, occ in enumerate(qamar_data, 1):
            f.write(f"  {i}. {occ['s']}:{occ['a']} - {occ['w']}\n")
        
        f.write("\n\n" + "=" * 60 + "\n")
        f.write("ÖZET\n")
        f.write("=" * 60 + "\n")
        f.write(f"Güneş (Şems): {len(shams_data)} ayet (Hedef: 33)\n")
        f.write(f"Ay (Kamer): {len(qamar_data)} ayet (Hedef: 27)\n")
        
        if len(shams_data) != 33:
            f.write(f"\n⚠️ UYARI: Güneş sayısı 33 değil, {len(shams_data)}! Eksik: {33 - len(shams_data)}\n")
        
        if len(qamar_data) != 27:
            f.write(f"\n⚠️ UYARI: Kamer sayısı 27 değil, {len(qamar_data)}! Eksik: {27 - len(qamar_data)}\n")
    
    print(f"Gunes (Sems): {len(shams_data)} ayet (Hedef: 33)")
    print(f"Ay (Kamer): {len(qamar_data)} ayet (Hedef: 27)")
    print("Detaylar: shams_qamar_analysis.txt")

if __name__ == '__main__':
    main()
