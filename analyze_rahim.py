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

def analyze_rahim_forms():
    """Rahim kelimesinin tüm formlarını analiz et"""
    if not os.path.exists(ARABIC_DATA_PATH):
        print("Arabic data file not found!")
        return

    with open(ARABIC_DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Rahim'in olası tüm formları
    rahim_forms = {
        'الرحيم': 0,   # Alif-Lam ile
        'رحيم': 0,     # Alif-Lam olmadan
        'رحيما': 0,    # Tenvin ile
        'الرحيمي': 0,  # Nisbet ile
    }
    
    for surah in data:
        for ayah in surah['verses']:
            text = clean_for_word_count(ayah['text'])
            
            for form in rahim_forms:
                rahim_forms[form] += text.count(form)
    
    print("Rahim Kelimesi Form Analizi:")
    print("="*50)
    for form, count in rahim_forms.items():
        print(f"{form}: {count}")
    
    total = sum(rahim_forms.values())
    print(f"\nToplam: {total}")
    
    # Edip Yüksel'in metoduna göre hangi form 114 (19x6) veriyor?
    print("\n19 Sistemi Kontrolü:")
    for form, count in rahim_forms.items():
        if count % 19 == 0:
            print(f"✅ {form}: {count} = 19 x {count // 19}")
        else:
            print(f"❌ {form}: {count} (Kalan: {count % 19})")
    
    return rahim_forms

if __name__ == "__main__":
    analyze_rahim_forms()
