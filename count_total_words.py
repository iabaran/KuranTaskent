#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Kur'an'da her kelimenin TOPLAM geçiş sayısını sayar (ayet başına değil, toplam kelime).
Bir ayette 3 kez geçiyorsa 3 olarak sayar.
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

def count_total_occurrences(quran, roots, name):
    """Count ALL occurrences of words, including multiple in same verse"""
    occurrences = []
    
    for surah in quran:
        surah_num = surah['id']
        for verse in surah.get('verses', []):
            verse_num = verse['id']
            text = verse['text']
            words = text.split()
            
            for word in words:
                normalized_word = normalize_arabic(word)
                for root in roots:
                    normalized_root = normalize_arabic(root)
                    if normalized_root in normalized_word:
                        occurrences.append({
                            's': surah_num,
                            'a': verse_num,
                            'w': word
                        })
                        break
    
    return occurrences

def main():
    quran = load_quran()
    
    # Kelime kökleri
    # Şems (شمس) - Tekil
    shams_roots = ['شمس']
    
    # Kamer (قمر) - Tekil
    qamar_roots = ['قمر']
    
    # Şehr (شهر) - Tekil ve Çoğul (أشهر / شهور)
    shehr_singular = ['شهر']
    shehr_plural = ['اشهر', 'أشهر', 'شهور']
    
    # Yevm (يوم) - Tekil ve Çoğul (أيام)
    yevm_singular = ['يوم']
    yevm_plural = ['ايام', 'أيام']
    
    # Sayımlar
    shams_data = count_total_occurrences(quran, shams_roots, 'Şems')
    qamar_data = count_total_occurrences(quran, qamar_roots, 'Kamer')
    shehr_s_data = count_total_occurrences(quran, shehr_singular, 'Şehr Tekil')
    shehr_p_data = count_total_occurrences(quran, shehr_plural, 'Şehr Çoğul')
    yevm_s_data = count_total_occurrences(quran, yevm_singular, 'Yevm Tekil')
    yevm_p_data = count_total_occurrences(quran, yevm_plural, 'Yevm Çoğul')
    
    # Sonuçları yazdır
    with open('total_word_counts.txt', 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write("TOPLAM KELİME SAYILARI (Her geçiş ayrı sayılır)\n")
        f.write("=" * 70 + "\n\n")
        
        # Şems
        f.write(f"Güneş (Şems) شمس\n")
        f.write("-" * 50 + "\n")
        f.write(f"  Toplam: {len(shams_data)}\n")
        for i, occ in enumerate(shams_data, 1):
            f.write(f"    {i}. {occ['s']}:{occ['a']} - {occ['w']}\n")
        f.write("\n")
        
        # Kamer
        f.write(f"Ay (Kamer) قمر\n")
        f.write("-" * 50 + "\n")
        f.write(f"  Toplam: {len(qamar_data)}\n")
        for i, occ in enumerate(qamar_data, 1):
            f.write(f"    {i}. {occ['s']}:{occ['a']} - {occ['w']}\n")
        f.write("\n")
        
        # Şehr
        shehr_total = len(shehr_s_data) + len(shehr_p_data)
        f.write(f"Ay (Şehr) شهر\n")
        f.write("-" * 50 + "\n")
        f.write(f"  Tekil: {len(shehr_s_data)}\n")
        f.write(f"  Çoğul: {len(shehr_p_data)}\n")
        f.write(f"  TOPLAM: {shehr_total}\n")
        f.write(f"\n  Tekil:\n")
        for i, occ in enumerate(shehr_s_data, 1):
            f.write(f"    {i}. {occ['s']}:{occ['a']} - {occ['w']}\n")
        f.write(f"\n  Çoğul:\n")
        for i, occ in enumerate(shehr_p_data, 1):
            f.write(f"    {i}. {occ['s']}:{occ['a']} - {occ['w']}\n")
        f.write("\n")
        
        # Yevm
        yevm_total = len(yevm_s_data) + len(yevm_p_data)
        f.write(f"Gün (Yevm) يوم\n")
        f.write("-" * 50 + "\n")
        f.write(f"  Tekil: {len(yevm_s_data)}\n")
        f.write(f"  Çoğul: {len(yevm_p_data)}\n")
        f.write(f"  TOPLAM: {yevm_total}\n")
        f.write(f"\n  Tekil:\n")
        for i, occ in enumerate(yevm_s_data, 1):
            f.write(f"    {i}. {occ['s']}:{occ['a']} - {occ['w']}\n")
        f.write(f"\n  Çoğul:\n")
        for i, occ in enumerate(yevm_p_data, 1):
            f.write(f"    {i}. {occ['s']}:{occ['a']} - {occ['w']}\n")
        
        f.write("\n\n" + "=" * 70 + "\n")
        f.write("ÖZET TABLO\n")
        f.write("=" * 70 + "\n")
        f.write(f"{'Kelime':<20} {'Tekil':>8} {'Çoğul':>8} {'Toplam':>8}\n")
        f.write("-" * 50 + "\n")
        f.write(f"{'Güneş (Şems)':<20} {len(shams_data):>8} {0:>8} {len(shams_data):>8}\n")
        f.write(f"{'Ay (Kamer)':<20} {len(qamar_data):>8} {0:>8} {len(qamar_data):>8}\n")
        f.write(f"{'Ay (Şehr)':<20} {len(shehr_s_data):>8} {len(shehr_p_data):>8} {shehr_total:>8}\n")
        f.write(f"{'Gün (Yevm)':<20} {len(yevm_s_data):>8} {len(yevm_p_data):>8} {yevm_total:>8}\n")
    
    # Generate JS data
    all_shehr = shehr_s_data + shehr_p_data
    all_yevm = yevm_s_data + yevm_p_data
    
    js_content = f"""// Generated automatically - TOTAL word occurrences (not unique verses)
// Each occurrence is counted separately

// Güneş (Şems) - Toplam: {len(shams_data)}
const shamsData = {json.dumps(shams_data, ensure_ascii=False)};

// Ay (Kamer) - Toplam: {len(qamar_data)}
const qamarData = {json.dumps(qamar_data, ensure_ascii=False)};

// Ay (Şehr) - Tekil: {len(shehr_s_data)}, Çoğul: {len(shehr_p_data)}, Toplam: {shehr_total}
const shehrData = {json.dumps(all_shehr, ensure_ascii=False)};

// Gün (Yevm) - Tekil: {len(yevm_s_data)}, Çoğul: {len(yevm_p_data)}, Toplam: {yevm_total}
const yevmData = {json.dumps(all_yevm, ensure_ascii=False)};
"""
    
    with open('shams_qamar_yevm_shehr_data.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    # Print summary
    print("\n" + "=" * 60)
    print("ÖZET (TOPLAM KELİME SAYILARI)")
    print("=" * 60)
    print(f"{'Kelime':<20} {'Tekil':>8} {'Çoğul':>8} {'Toplam':>8}")
    print("-" * 50)
    print(f"{'Gunes (Sems)':<20} {len(shams_data):>8} {0:>8} {len(shams_data):>8}")
    print(f"{'Ay (Kamer)':<20} {len(qamar_data):>8} {0:>8} {len(qamar_data):>8}")
    print(f"{'Ay (Shehr)':<20} {len(shehr_s_data):>8} {len(shehr_p_data):>8} {shehr_total:>8}")
    print(f"{'Gun (Yevm)':<20} {len(yevm_s_data):>8} {len(yevm_p_data):>8} {yevm_total:>8}")
    print("\nDetaylar: total_word_counts.txt")

if __name__ == '__main__':
    main()
