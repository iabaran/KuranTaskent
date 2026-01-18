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

def analyze_rahim_all_forms():
    """Rahim'in TÜM formlarını say"""
    if not os.path.exists(ARABIC_DATA_PATH):
        print("Arabic data file not found!")
        return

    with open(ARABIC_DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    forms = {
        'الرحيم': 0,    # Standart
        'رحيم': 0,      # Alif-Lam olmadan
        'رحيما': 0,     # Tenvin (accusative)
        'رحيمة': 0,     # Feminine
        'الرحيمة': 0,   # Feminine + Alif-Lam
    }
    
    for surah in data:
        for ayah in surah['verses']:
            text = clean_for_word_count(ayah['text'])
            
            # Her formu say (çakışmaları önlemek için sıralı)
            forms['الرحيمة'] += text.count('الرحيمة')
            forms['رحيمة'] += text.replace('الرحيمة', '').count('رحيمة')
            forms['الرحيم'] += text.replace('الرحيمة', '').count('الرحيم')
            forms['رحيما'] += text.count('رحيما')
            
            # رحيم sayımı (diğer formlar hariç)
            temp = text.replace('الرحيم', '').replace('رحيما', '').replace('رحيمة', '').replace('الرحيمة', '')
            forms['رحيم'] += temp.count('رحيم')
    
    print("Rahim - TÜM Form Analizi:")
    print("="*50)
    for form, count in forms.items():
        if count > 0:
            print(f"{form}: {count}")
    
    # Farklı kombinasyonları dene
    print("\nFarklı Kombinasyonlar:")
    
    # 1. Sadece الرحيم + رحيم
    combo1 = forms['الرحيم'] + forms['رحيم']
    print(f"الرحيم + رحيم = {combo1}")
    if combo1 == 114:
        print("  ✅ TAM 114!")
    
    # 2. Tenvin hariç
    combo2 = forms['الرحيم'] + forms['رحيم'] + forms['رحيمة'] + forms['الرحيمة']
    print(f"Tenvin (رحيما) hariç = {combo2}")
    if combo2 == 114:
        print("  ✅ TAM 114!")
    
    # 3. Sadece الرحيم + رحيم + رحيما
    combo3 = forms['الرحيم'] + forms['رحيم'] + forms['رحيما']
    print(f"الرحيم + رحيم + رحيما = {combo3}")
    if combo3 == 114:
        print("  ✅ TAM 114!")
    
    total = sum(forms.values())
    print(f"\nGenel Toplam: {total}")
    
    return forms

if __name__ == "__main__":
    analyze_rahim_all_forms()
