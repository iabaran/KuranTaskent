#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Kur'an'da "gün" anlamına gelen tüm kelime formlarını detaylı analiz eder.
365 rakamına nasıl ulaşıldığını araştırır.
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

def analyze_yevm_forms(quran):
    """Analyze all forms of 'day' word in Quran"""
    
    # Different forms:
    # يوم (yevm) - day (tekil, merfû)
    # يوما (yevmen) - day (tekil, mansûb)
    # يومئذ (yevme-izin) - that day (özel form)
    # أيام (eyyâm) - days (çoğul)
    # يومهم (yevmuhum) - their day
    # يومكم (yevmukum) - your day
    
    forms = {
        'يوم': {'name': 'يوم (yevm - tekil)', 'count': 0, 'verses': []},
        'يوما': {'name': 'يوماً (yevmen - tekil mansub)', 'count': 0, 'verses': []},
        'يومئذ': {'name': 'يومئذ (yevme-izin - o gün)', 'count': 0, 'verses': []},
        'ايام': {'name': 'أيام (eyyam - çoğul)', 'count': 0, 'verses': []},
        'يومهم': {'name': 'يومهم (yevmuhum - onların günü)', 'count': 0, 'verses': []},
        'يومكم': {'name': 'يومكم (yevmukum - sizin gününüz)', 'count': 0, 'verses': []},
        'يومه': {'name': 'يومه (yevmuh)', 'count': 0, 'verses': []},
        'يومها': {'name': 'يومها (yevmuha)', 'count': 0, 'verses': []},
        'يومين': {'name': 'يومين (yevmeyn - iki gün)', 'count': 0, 'verses': []},
    }
    
    all_day_words = []
    
    for surah in quran:
        surah_num = surah['id']
        for verse in surah.get('verses', []):
            verse_num = verse['id']
            text = verse['text']
            words = text.split()
            
            for word in words:
                normalized = normalize_arabic(word)
                
                # Check each form
                matched = False
                for form_key in forms.keys():
                    if normalize_arabic(form_key) in normalized:
                        forms[form_key]['count'] += 1
                        forms[form_key]['verses'].append(f"{surah_num}:{verse_num}")
                        all_day_words.append({
                            's': surah_num,
                            'a': verse_num,
                            'w': word,
                            'form': form_key
                        })
                        matched = True
                        break
                
                # If not matched, check if it contains يوم root
                if not matched and 'يوم' in normalized:
                    print(f"Unclassified: {word} at {surah_num}:{verse_num}")
    
    return forms, all_day_words

def main():
    quran = load_quran()
    forms, all_words = analyze_yevm_forms(quran)
    
    with open('yevm_detailed_analysis.txt', 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write("GÜN (YEVM) KELİMESİ DETAYLI ANALİZ\n")
        f.write("=" * 70 + "\n\n")
        
        total = 0
        tekil_total = 0
        cogul_total = 0
        
        for form_key, data in forms.items():
            if data['count'] > 0:
                f.write(f"\n{data['name']}\n")
                f.write("-" * 50 + "\n")
                f.write(f"  Sayı: {data['count']}\n")
                f.write(f"  Ayetler: {', '.join(data['verses'][:20])}")
                if len(data['verses']) > 20:
                    f.write(f"... (+{len(data['verses'])-20} daha)")
                f.write("\n")
                total += data['count']
                
                if 'çoğul' in data['name'].lower() or 'ايام' in form_key:
                    cogul_total += data['count']
                else:
                    tekil_total += data['count']
        
        f.write("\n\n" + "=" * 70 + "\n")
        f.write("ÖZET\n")
        f.write("=" * 70 + "\n")
        
        f.write(f"\nTekil formlar toplamı: {tekil_total}\n")
        f.write(f"Çoğul formlar toplamı: {cogul_total}\n")
        f.write(f"GENEL TOPLAM: {total}\n")
        
        f.write("\n\n" + "=" * 70 + "\n")
        f.write("365 HESABI HAKKINDA\n")
        f.write("=" * 70 + "\n")
        f.write("""
365 sayısı için yaygın kullanılan metodoloji:
- Sadece TEKİL form (يوم) sayılır
- Çoğul form (أيام) HARİÇ tutulur
- يومئذ (yevme-izin = o gün) bazen dahil bazen hariç tutulur

Bizim sayımımız:
- Her kelime geçişi ayrı sayılır
- Tüm formlar dahil edilir

NOT: Farklı mushaf baskıları ve sayım metodolojileri 
farklı sonuçlar verebilir. 365 iddiası tartışmalıdır.
""")
    
    # Print summary
    print("\n" + "=" * 60)
    print("GÜN (YEVM) ÖZET")
    print("=" * 60)
    
    total = 0
    tekil = 0
    cogul = 0
    
    for form_key, data in forms.items():
        if data['count'] > 0:
            print(f"{data['name']}: {data['count']}")
            total += data['count']
            if 'çoğul' in data['name'].lower() or 'ايام' in form_key:
                cogul += data['count']
            else:
                tekil += data['count']
    
    print("-" * 60)
    print(f"Tekil toplam: {tekil}")
    print(f"Cogul toplam: {cogul}")
    print(f"GENEL TOPLAM: {total}")
    print("\nDetaylar: yevm_detailed_analysis.txt")

if __name__ == '__main__':
    main()
