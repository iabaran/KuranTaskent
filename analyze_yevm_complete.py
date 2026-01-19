#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Kur'an'da "يوم" kökünü içeren TÜM kelimeleri bulur ve kategorize eder.
"""

import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

def load_quran():
    with open('quran_arabic.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def normalize_arabic(text):
    """Remove all diacritics"""
    diacritics = re.compile(r'[\u064B-\u065F\u0670\u06D6-\u06ED\u0640\u0653-\u0655]')
    return diacritics.sub('', text)

def main():
    quran = load_quran()
    
    # يوم kökü (tekil)
    yevm_root = normalize_arabic('يوم')
    # أيام kökü (çoğul)
    ayyam_root = normalize_arabic('ايام')
    
    yevm_words = {}  # Tekil formlar
    ayyam_words = {}  # Çoğul formlar
    
    yevm_total = 0
    ayyam_total = 0
    
    yevm_list = []
    ayyam_list = []
    
    for surah in quran:
        surah_num = surah['id']
        for verse in surah.get('verses', []):
            verse_num = verse['id']
            text = verse['text']
            words = text.split()
            
            for word in words:
                normalized = normalize_arabic(word)
                
                # Check for çoğul (أيام) first - more specific
                if ayyam_root in normalized:
                    ayyam_total += 1
                    if word not in ayyam_words:
                        ayyam_words[word] = 0
                    ayyam_words[word] += 1
                    ayyam_list.append({'s': surah_num, 'a': verse_num, 'w': word})
                
                # Check for tekil (يوم) - less specific, avoid double counting
                elif yevm_root in normalized:
                    yevm_total += 1
                    if word not in yevm_words:
                        yevm_words[word] = 0
                    yevm_words[word] += 1
                    yevm_list.append({'s': surah_num, 'a': verse_num, 'w': word})
    
    with open('yevm_complete_analysis.txt', 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write("GÜN (YEVM) KOMPLİT ANALİZ\n")
        f.write("=" * 70 + "\n\n")
        
        f.write("TEKİL FORMLAR (يوم kökü):\n")
        f.write("-" * 50 + "\n")
        for word, count in sorted(yevm_words.items(), key=lambda x: -x[1]):
            f.write(f"  {word}: {count} kez\n")
        f.write(f"\n  TOPLAM TEKİL: {yevm_total}\n")
        
        f.write("\n\nÇOĞUL FORMLAR (أيام kökü):\n")
        f.write("-" * 50 + "\n")
        for word, count in sorted(ayyam_words.items(), key=lambda x: -x[1]):
            f.write(f"  {word}: {count} kez\n")
        f.write(f"\n  TOPLAM ÇOĞUL: {ayyam_total}\n")
        
        f.write(f"\n\n{'='*70}\n")
        f.write(f"GENEL TOPLAM: {yevm_total + ayyam_total}\n")
        f.write(f"{'='*70}\n")
        
        f.write(f"\n\nTEKİL AYETLER ({yevm_total} adet):\n")
        f.write("-" * 50 + "\n")
        for i, item in enumerate(yevm_list, 1):
            f.write(f"  {i}. {item['s']}:{item['a']} - {item['w']}\n")
        
        f.write(f"\n\nÇOĞUL AYETLER ({ayyam_total} adet):\n")
        f.write("-" * 50 + "\n")
        for i, item in enumerate(ayyam_list, 1):
            f.write(f"  {i}. {item['s']}:{item['a']} - {item['w']}\n")
    
    print("=" * 60)
    print("GÜN (YEVM) KOMPLİT ANALİZ")
    print("=" * 60)
    
    print("\nTEKİL FORMLAR:")
    for word, count in sorted(yevm_words.items(), key=lambda x: -x[1])[:10]:
        print(f"  {word}: {count}")
    if len(yevm_words) > 10:
        print(f"  ... (+{len(yevm_words)-10} daha)")
    print(f"  TOPLAM TEKIL: {yevm_total}")
    
    print("\nCOGUL FORMLAR:")
    for word, count in sorted(ayyam_words.items(), key=lambda x: -x[1]):
        print(f"  {word}: {count}")
    print(f"  TOPLAM COGUL: {ayyam_total}")
    
    print("\n" + "-" * 60)
    print(f"GENEL TOPLAM: {yevm_total + ayyam_total}")
    print("-" * 60)
    
    print("\nDetaylar: yevm_complete_analysis.txt")

if __name__ == '__main__':
    main()
