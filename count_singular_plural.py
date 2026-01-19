#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Kur'an'da Şems, Kamer, Şehr ve Yevm kelimelerini TEKİL ve ÇOĞUL olarak ayırarak sayar.
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

def find_word_forms(quran, singular_roots, plural_roots, name):
    """Find singular and plural forms separately"""
    singular_data = []
    plural_data = []
    
    for surah in quran:
        surah_num = surah['id']
        for verse in surah.get('verses', []):
            verse_num = verse['id']
            text = verse['text']
            normalized = normalize_arabic(text)
            
            # Check singular
            found_singular = False
            for root in singular_roots:
                if normalize_arabic(root) in normalized:
                    singular_data.append({'s': surah_num, 'a': verse_num, 'w': root})
                    found_singular = True
                    break
            
            # Check plural (only if singular not found to avoid double counting)
            if not found_singular:
                for root in plural_roots:
                    if normalize_arabic(root) in normalized:
                        plural_data.append({'s': surah_num, 'a': verse_num, 'w': root})
                        break
    
    return singular_data, plural_data

def main():
    quran = load_quran()
    
    # === ŞEMS (Güneş) ===
    # Tekil: شمس
    # Çoğul: شموس (kullanılmamış olabilir)
    shams_singular = ['شمس']
    shams_plural = ['شموس']
    
    # === KAMER (Ay) ===
    # Tekil: قمر
    # Çoğul: أقمار (kullanılmamış olabilir)
    qamar_singular = ['قمر']
    qamar_plural = ['اقمار', 'أقمار']
    
    # === ŞEHR (Ay/Month) ===
    # Tekil: شهر
    # Çoğul: أشهر / شهور
    shehr_singular = ['شهر']
    shehr_plural = ['اشهر', 'أشهر', 'شهور']
    
    # === YEVM (Gün) ===
    # Tekil: يوم
    # Çoğul: أيام
    yevm_singular = ['يوم']
    yevm_plural = ['ايام', 'أيام']
    
    results = {}
    
    # Count Shams
    shams_s, shams_p = find_word_forms(quran, shams_singular, shams_plural, 'Şems')
    results['shams'] = {'singular': shams_s, 'plural': shams_p, 'name': 'Güneş (Şems)', 'ar': 'شمس'}
    
    # Count Qamar
    qamar_s, qamar_p = find_word_forms(quran, qamar_singular, qamar_plural, 'Kamer')
    results['qamar'] = {'singular': qamar_s, 'plural': qamar_p, 'name': 'Ay (Kamer)', 'ar': 'قمر'}
    
    # Count Shehr
    shehr_s, shehr_p = find_word_forms(quran, shehr_singular, shehr_plural, 'Şehr')
    results['shehr'] = {'singular': shehr_s, 'plural': shehr_p, 'name': 'Ay (Şehr)', 'ar': 'شهر'}
    
    # Count Yevm
    yevm_s, yevm_p = find_word_forms(quran, yevm_singular, yevm_plural, 'Yevm')
    results['yevm'] = {'singular': yevm_s, 'plural': yevm_p, 'name': 'Gün (Yevm)', 'ar': 'يوم'}
    
    # Write results
    with open('singular_plural_counts.txt', 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write("TEKİL VE ÇOĞUL SAYILARI\n")
        f.write("=" * 70 + "\n\n")
        
        for key, data in results.items():
            s_count = len(data['singular'])
            p_count = len(data['plural'])
            total = s_count + p_count
            
            f.write(f"\n{data['name']} ({data['ar']})\n")
            f.write("-" * 50 + "\n")
            f.write(f"  Tekil  : {s_count}\n")
            f.write(f"  Çoğul  : {p_count}\n")
            f.write(f"  TOPLAM : {total}\n")
            
            if s_count > 0:
                f.write(f"\n  Tekil ayetler:\n")
                for i, occ in enumerate(data['singular'], 1):
                    f.write(f"    {i}. {occ['s']}:{occ['a']}\n")
            
            if p_count > 0:
                f.write(f"\n  Çoğul ayetler:\n")
                for i, occ in enumerate(data['plural'], 1):
                    f.write(f"    {i}. {occ['s']}:{occ['a']}\n")
            
            f.write("\n")
        
        f.write("\n" + "=" * 70 + "\n")
        f.write("ÖZET TABLO\n")
        f.write("=" * 70 + "\n")
        f.write(f"{'Kelime':<20} {'Tekil':>8} {'Çoğul':>8} {'Toplam':>8}\n")
        f.write("-" * 50 + "\n")
        
        for key, data in results.items():
            s = len(data['singular'])
            p = len(data['plural'])
            t = s + p
            f.write(f"{data['name']:<20} {s:>8} {p:>8} {t:>8}\n")
    
    # Generate JS data file with separate arrays
    js_content = """// Generated automatically - Singular and Plural forms separated

"""
    
    for key, data in results.items():
        s_count = len(data['singular'])
        p_count = len(data['plural'])
        total = s_count + p_count
        
        # Singular data
        js_content += f"// {data['name']} - Tekil: {s_count}, Çoğul: {p_count}, Toplam: {total}\n"
        js_content += f"const {key}Data = [\n"
        
        all_data = data['singular'] + data['plural']
        for occ in all_data:
            js_content += f"  {{ s: {occ['s']}, a: {occ['a']}, w: \"{occ['w']}\" }},\n"
        
        js_content += "];\n\n"
    
    with open('shams_qamar_yevm_shehr_data.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    # Print summary
    print("\n" + "=" * 60)
    print("ÖZET")
    print("=" * 60)
    print(f"{'Kelime':<20} {'Tekil':>8} {'Çoğul':>8} {'Toplam':>8}")
    print("-" * 50)
    
    for key, data in results.items():
        s = len(data['singular'])
        p = len(data['plural'])
        t = s + p
        print(f"{data['name']:<20} {s:>8} {p:>8} {t:>8}")
    
    print("\nDetaylar: singular_plural_counts.txt")
    print("JS dosyasi: shams_qamar_yevm_shehr_data.js")

if __name__ == '__main__':
    main()
