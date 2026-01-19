#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Şems ve Kamer için eksik ayetleri bulmak amacıyla kapsamlı arama
"""

import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

def load_quran():
    with open('quran_arabic.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def normalize_arabic(text):
    """Remove all diacritics for matching"""
    diacritics = re.compile(r'[\u064B-\u065F\u0670\u06D6-\u06ED\u0640\u0653-\u0655]')
    return diacritics.sub('', text)

def main():
    quran = load_quran()
    
    # Known missing verse candidates for verification
    # Common verses mentioned in "33 shams" lists
    potential_shams = [
        (2, 258), (6, 78), (6, 96), (7, 54), (10, 5), (12, 4), (13, 2), 
        (14, 33), (16, 12), (17, 78), (18, 17), (18, 86), (18, 90), 
        (20, 130), (21, 33), (22, 18), (25, 45), (27, 24), (29, 61), 
        (31, 29), (35, 13), (36, 38), (36, 40), (39, 5), (41, 37), 
        (50, 39), (55, 5), (71, 16), (75, 9), (76, 13), (81, 1), (91, 1)
        # That's 32 - need to find the 33rd
    ]
    
    # Additional candidates - check for alternate roots
    possible_sunlight_words = ['ضياء', 'ضوء', 'سراج', 'مشرق', 'مغرب']
    
    print("Analyzing for potentially missed sun-related verses...")
    
    with open('shams_qamar_deep_analysis.txt', 'w', encoding='utf-8') as f:
        f.write("DEEP ANALYSIS: Looking for missed شمس occurrences\n")
        f.write("=" * 60 + "\n\n")
        
        # Check what we have
        shams_count = 0
        for surah in quran:
            surah_num = surah['id']
            for verse in surah.get('verses', []):
                verse_num = verse['id']
                text = verse['text']
                normalized = normalize_arabic(text)
                
                # Check for شمس in any form
                if 'شمس' in normalized:
                    shams_count += 1
                    f.write(f"  SHAMS {shams_count}: {surah_num}:{verse_num}\n")
        
        f.write(f"\nTotal شمس: {shams_count}\n")
        
        f.write("\n\n" + "=" * 60 + "\n")
        f.write("DEEP ANALYSIS: Looking for missed قمر occurrences\n")
        f.write("=" * 60 + "\n\n")
        
        # Check what we have for qamar
        qamar_count = 0
        for surah in quran:
            surah_num = surah['id']
            for verse in surah.get('verses', []):
                verse_num = verse['id']
                text = verse['text']
                normalized = normalize_arabic(text)
                
                # Check for قمر in any form
                if 'قمر' in normalized:
                    qamar_count += 1
                    f.write(f"  QAMAR {qamar_count}: {surah_num}:{verse_num}\n")
        
        f.write(f"\nTotal قمر: {qamar_count}\n")
        
        f.write("\n\n" + "=" * 60 + "\n")
        f.write("CONCLUSION\n")
        f.write("=" * 60 + "\n")
        f.write(f"شمس (Shams/Sun): {shams_count} verses\n")
        f.write(f"قمر (Qamar/Moon): {qamar_count} verses\n")
        f.write("\nNote: The '33 and 27' counts might include:\n")
        f.write("- Different counting methodologies\n")
        f.write("- Counting individual word occurrences (some verses may have 2 mentions)\n")
        f.write("- Different Quran text editions\n")
    
    print(f"Shams: {shams_count}")
    print(f"Qamar: {qamar_count}")
    print("Details: shams_qamar_deep_analysis.txt")

if __name__ == '__main__':
    main()
