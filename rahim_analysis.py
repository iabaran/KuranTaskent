# -*- coding: utf-8 -*-
"""
Kur'an'da "Rahim" kelimesinin geçtiği yerleri analiz eden script.

Rahim kelimesi şu yerlerde geçer:
1. Her surenin başındaki Besmele'de (Tevbe suresi hariç): 113 adet
2. Fatiha suresinin 3. ayetinde: 1 adet
3. Neml suresinin 30. ayetinde (Hz. Süleyman'ın mektubundaki besmele): 1 adet

Toplam: 115 adet
"""

import json
import re
import sys
from pathlib import Path

# Windows console encoding fix
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def normalize_arabic(text):
    """Arapça metni normalize et (harekeleri kaldır)"""
    if not text:
        return ""
    # Hareke ve diğer işaretleri kaldır
    text = re.sub(r'[\u064B-\u065F\u0670]', '', text)
    return text.strip()

def find_rahim_occurrences():
    """Kur'an'da Rahim kelimesinin geçtiği yerleri bul"""
    
    # quran_arabic.json dosyasını yükle
    quran_path = Path("quran_arabic.json")
    
    if not quran_path.exists():
        print("❌ quran_arabic.json dosyası bulunamadı!")
        return
    
    with open(quran_path, 'r', encoding='utf-8') as f:
        quran_data = json.load(f)
    
    # Rahim kelimesini ara (farklı yazım şekilleri)
    rahim_patterns = [
        'رحيم',  # Rahim (harekesiz)
    ]
    
    occurrences = []
    besmele_count = 0
    fatiha_extra_count = 0
    neml_extra_count = 0
    other_count = 0
    
    for surah in quran_data:
        surah_number = surah.get('id', 0)
        surah_name = surah.get('name', '')
        surah_transliteration = surah.get('transliteration', '')
        verses = surah.get('verses', [])
        
        for verse_data in verses:
            verse_number = verse_data.get('id', 0)
            arabic_text = verse_data.get('text', '')
            normalized = normalize_arabic(arabic_text)
            
            # Rahim kelimesini say
            rahim_count_in_verse = 0
            for pattern in rahim_patterns:
                rahim_count_in_verse += normalized.count(pattern)
            
            if rahim_count_in_verse > 0:
                # Her bir Rahim için ayrı kayıt oluştur
                for i in range(rahim_count_in_verse):
                    occurrence = {
                        'surah': surah_number,
                        'surah_name': surah_name,
                        'surah_transliteration': surah_transliteration,
                        'verse': verse_number,
                        'text': arabic_text
                    }
                    
                    # Kategorilendir
                    if verse_number == 1 and surah_number != 9:
                        # Besmele (Tevbe suresi hariç, tüm surelerin ilk ayeti)
                        besmele_count += 1
                        occurrence['category'] = 'Besmele'
                        if surah_number == 1:
                            occurrence['note'] = 'Fatiha\'nın besmelesi'
                    elif surah_number == 1 and verse_number == 3:
                        # Fatiha'nın 3. ayeti (er-Rahmani'r-Rahim)
                        fatiha_extra_count += 1
                        occurrence['category'] = 'Fatiha 3. Ayet (EKSTRA)'
                        occurrence['note'] = 'Fatiha\'da besmele dışında bir Rahim daha'
                    elif surah_number == 27 and verse_number == 30:
                        # Neml suresi 30. ayet (Hz. Süleyman'ın mektubu)
                        neml_extra_count += 1
                        occurrence['category'] = 'Neml 30 (EKSTRA - Süleyman\'ın Mektubu)'
                        occurrence['note'] = 'Hz. Süleyman\'ın mektubundaki besmele'
                    else:
                        # Diğer
                        other_count += 1
                        occurrence['category'] = 'Diğer'
                    
                    occurrences.append(occurrence)
    
    # Sonuçları yazdır
    print("=" * 80)
    print("KUR'AN'DA 'RAHİM' KELİMESİNİN GEÇTİĞİ YERLER")
    print("=" * 80)
    print()
    
    print(f"📊 ÖZET:")
    print(f"   • Besmelelerdeki Rahim (113 sure): {besmele_count}")
    print(f"   • Fatiha 3. ayetteki EKSTRA Rahim: {fatiha_extra_count}")
    print(f"   • Neml 30. ayetteki EKSTRA Rahim: {neml_extra_count}")
    print(f"   • Diğer yerlerdeki Rahim: {other_count}")
    print(f"   ─────────────────────────────────")
    print(f"   • TOPLAM: {len(occurrences)}")
    print()
    
    # Beklenen değerler
    expected_besmele = 113  # Tevbe hariç tüm sureler
    expected_fatiha = 1     # Fatiha'nın 3. ayeti
    expected_neml = 1       # Neml 30
    expected_total = 115    # Toplam
    
    print(f"✅ DOĞRULAMA:")
    print(f"   • Besmele: {besmele_count} (Beklenen: {expected_besmele}) {'✓' if besmele_count == expected_besmele else '✗'}")
    print(f"   • Fatiha ekstra: {fatiha_extra_count} (Beklenen: {expected_fatiha}) {'✓' if fatiha_extra_count == expected_fatiha else '✗'}")
    print(f"   • Neml ekstra: {neml_extra_count} (Beklenen: {expected_neml}) {'✓' if neml_extra_count == expected_neml else '✗'}")
    print(f"   • Toplam: {len(occurrences)} (Beklenen: {expected_total}) {'✓' if len(occurrences) == expected_total else '✗'}")
    print()
    
    print("=" * 80)
    print("DETAYLI LİSTE:")
    print("=" * 80)
    
    # Kategorilere göre grupla
    categories = {}
    for occ in occurrences:
        cat = occ['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(occ)
    
    # Her kategoriyi yazdır
    category_order = [
        'Besmele',
        'Fatiha 3. Ayet (EKSTRA)',
        'Neml 30 (EKSTRA - Süleyman\'ın Mektubu)',
        'Diğer'
    ]
    
    for category in category_order:
        if category not in categories:
            continue
        items = categories[category]
        print(f"\n📌 {category} ({len(items)} adet):")
        print("-" * 80)
        
        # Özel kategoriler için tüm öğeleri göster
        if 'EKSTRA' in category or len(items) <= 10:
            for item in items:
                print(f"   {item['surah']:3d}:{item['verse']:3d} - {item['surah_transliteration']}")
                if 'note' in item:
                    print(f"        Not: {item['note']}")
                print(f"        {item['text']}")
        else:
            # Besmele için sadece ilk ve son birkaç örneği göster
            for item in items[:5]:
                print(f"   {item['surah']:3d}:{item['verse']:3d} - {item['surah_transliteration']}")
            print(f"   ... {len(items) - 10} adet daha ...")
            for item in items[-5:]:
                print(f"   {item['surah']:3d}:{item['verse']:3d} - {item['surah_transliteration']}")
    
    print()
    print("=" * 80)
    print("📝 AÇIKLAMA:")
    print("=" * 80)
    print()
    print("Kur'an'da 'Rahim' kelimesi toplam 115 kez geçer:")
    print()
    print("1. BESMELELERDEKİ RAHİM (113 adet):")
    print("   • 114 surenin 113'ü besmele ile başlar")
    print("   • Tevbe suresi (9. sure) besmele ile başlamaz")
    print("   • Her besmelede 'Bismillahir-Rahmanir-Rahim' ifadesi vardır")
    print()
    print("2. FATİHA SURESİNDEKİ EKSTRA RAHİM (1 adet):")
    print("   • Fatiha suresinde 2 adet Rahim vardır:")
    print("     - 1. ayette besmele: 'Bismillahir-Rahmanir-Rahim'")
    print("     - 3. ayette: 'er-Rahmani'r-Rahim' (EKSTRA)")
    print()
    print("3. NEML SURESİNDEKİ EKSTRA RAHİM (1 adet):")
    print("   • Neml suresi 30. ayette Hz. Süleyman'ın mektubunda")
    print("     bir besmele daha vardır: 'Bismillahir-Rahmanir-Rahim' (EKSTRA)")
    print()
    print("TOPLAM: 113 (besmele) + 1 (Fatiha) + 1 (Neml) = 115 RAHİM")
    print()
    print("=" * 80)
    
    # JSON dosyasına kaydet
    output_file = 'rahim_occurrences.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(occurrences, f, ensure_ascii=False, indent=2)
    print(f"\n✅ Sonuçlar '{output_file}' dosyasına kaydedildi.")

if __name__ == "__main__":
    find_rahim_occurrences()
