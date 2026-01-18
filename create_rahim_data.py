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

def create_rahim_data():
    """Rahim kelimesinin tüm geçişlerini JSON olarak kaydet"""
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
            
            # الرحيم
            if 'الرحيم' in text:
                occurrences.append({
                    'surah': surah_num,
                    'ayah': ayah_num,
                    'form': 'الرحيم'
                })
            
            # رحيما
            if 'رحيما' in text:
                occurrences.append({
                    'surah': surah_num,
                    'ayah': ayah_num,
                    'form': 'رحيما'
                })
            
            # رحيم (diğerleri hariç)
            temp = text.replace('الرحيم', '').replace('رحيما', '')
            if 'رحيم' in temp:
                occurrences.append({
                    'surah': surah_num,
                    'ayah': ayah_num,
                    'form': 'رحيم'
                })
    
    # JSON olarak kaydet
    output = {
        'total': len(occurrences),
        'occurrences': occurrences
    }
    
    with open('d:/KuranTaskent/rahim_occurrences.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"✅ {len(occurrences)} Rahim geçişi 'rahim_occurrences.json' dosyasına kaydedildi.")
    
    # Özet
    by_form = {}
    for occ in occurrences:
        form = occ['form']
        by_form[form] = by_form.get(form, 0) + 1
    
    print("\nForm Dağılımı:")
    for form, count in by_form.items():
        print(f"  {form}: {count}")
    
    return output

if __name__ == "__main__":
    create_rahim_data()
