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

def list_all_rahim_occurrences():
    """Rahim kelimesinin tüm geçişlerini listele"""
    if not os.path.exists(ARABIC_DATA_PATH):
        print("Arabic data file not found!")
        return

    with open(ARABIC_DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    occurrences = []
    
    for surah in data:
        surah_num = surah['id']
        surah_name = surah.get('name', f'Sure {surah_num}')
        
        for ayah in surah['verses']:
            ayah_num = ayah['id']
            text = clean_for_word_count(ayah['text'])
            
            # الرحيم kontrolü
            if 'الرحيم' in text:
                occurrences.append({
                    'surah': surah_num,
                    'surah_name': surah_name,
                    'ayah': ayah_num,
                    'form': 'الرحيم',
                    'location': f"{surah_num}:{ayah_num}"
                })
            
            # رحيما kontrolü
            if 'رحيما' in text:
                occurrences.append({
                    'surah': surah_num,
                    'surah_name': surah_name,
                    'ayah': ayah_num,
                    'form': 'رحيما',
                    'location': f"{surah_num}:{ayah_num}"
                })
            
            # رحيم kontrolü (الرحيم ve رحيما hariç)
            temp = text.replace('الرحيم', '').replace('رحيما', '')
            if 'رحيم' in temp:
                occurrences.append({
                    'surah': surah_num,
                    'surah_name': surah_name,
                    'ayah': ayah_num,
                    'form': 'رحيم',
                    'location': f"{surah_num}:{ayah_num}"
                })
    
    # Gruplama
    by_form = {}
    for occ in occurrences:
        form = occ['form']
        if form not in by_form:
            by_form[form] = []
        by_form[form].append(occ)
    
    print("Rahim Kelimesi - Tüm Geçişler:")
    print("="*70)
    
    for form, items in by_form.items():
        print(f"\n{form} ({len(items)} kez):")
        print("-" * 70)
        for i, item in enumerate(items, 1):
            print(f"{i:3}. Sure {item['surah']:3} ({item['surah_name'][:20]:20}), Ayet {item['ayah']:3}")
    
    print("\n" + "="*70)
    total = sum(len(items) for items in by_form.values())
    print(f"TOPLAM: {total}")
    
    if total == 114:
        print("✅ TAM 114! (19 x 6)")
    elif total == 115:
        print("❌ 115 (1 fazla)")
    else:
        print(f"Fark: {abs(total - 114)}")
    
    return occurrences

if __name__ == "__main__":
    list_all_rahim_occurrences()
