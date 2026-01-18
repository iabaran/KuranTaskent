import json
import os
import re
import sys

# Set encoding for Windows terminal
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

# Dosya yolları
ARABIC_DATA_PATH = r"d:\KuranTaskent\quran_arabic.json"

def clean_for_word_count(text):
    """Kelime sayımı için: Diyakritikleri temizle"""
    normalized = re.sub(r'[\u064B-\u0652\u06D6-\u06DC\u06DF-\u06E8\u06EA-\u06ED]', '', text)
    # Alif Wasla -> Alif
    normalized = normalized.replace('ٱ', 'ا')
    return normalized.strip()

def find_rahim_occurrences():
    """Rahim kelimesinin her geçtiği yeri listele"""
    if not os.path.exists(ARABIC_DATA_PATH):
        print("Arabic data file not found!")
        return

    with open(ARABIC_DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    occurrences = []
    
    for surah in data:
        surah_num = surah['id']
        for ayah in surah['verses']:
            ayah_num = ayah['id']
            text = clean_for_word_count(ayah['text'])
            
            # الرحيم sayımı
            if 'الرحيم' in text:
                count = text.count('الرحيم')
                occurrences.append({
                    'surah': surah_num,
                    'ayah': ayah_num,
                    'form': 'الرحيم',
                    'count': count
                })
            
            # رحيم sayımı (الرحيم hariç)
            temp_text = text.replace('الرحيم', '')
            if 'رحيم' in temp_text:
                count = temp_text.count('رحيم')
                occurrences.append({
                    'surah': surah_num,
                    'ayah': ayah_num,
                    'form': 'رحيم',
                    'count': count
                })
    
    # Toplam sayıları hesapla
    total_al_rahim = sum(o['count'] for o in occurrences if o['form'] == 'الرحيم')
    total_rahim = sum(o['count'] for o in occurrences if o['form'] == 'رحيم')
    
    print("Rahim Kelimesi Geçiş Analizi:")
    print("="*50)
    print(f"الرحيم toplam: {total_al_rahim}")
    print(f"رحيم toplam: {total_rahim}")
    print(f"Genel Toplam: {total_al_rahim + total_rahim}")
    
    # Birden fazla geçen ayetleri göster
    print("\nBirden Fazla Geçen Ayetler:")
    for occ in occurrences:
        if occ['count'] > 1:
            print(f"  Sure {occ['surah']}, Ayet {occ['ayah']}: {occ['form']} x{occ['count']}")
    
    # 19 kontrolü
    total = total_al_rahim + total_rahim
    print(f"\n19 Sistemi Kontrolü:")
    print(f"Toplam: {total}")
    if total == 114:
        print(f"✅ TAM 114! (19 x 6)")
    elif total == 115:
        print(f"❌ 115 çıktı (114 olmalı, 1 fazla)")
        print(f"   Belki bir ayet çift sayılıyor veya özel bir durum var")
    else:
        print(f"Fark: {abs(total - 114)}")
    
    return occurrences

if __name__ == "__main__":
    find_rahim_occurrences()
