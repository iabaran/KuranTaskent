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

def analyze_rahim_detailed():
    """Rahim kelimesini detaylı analiz et"""
    if not os.path.exists(ARABIC_DATA_PATH):
        print("Arabic data file not found!")
        return

    with open(ARABIC_DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # İki ana form
    count_al_rahim = 0  # الرحيم (Alif-Lam ile)
    count_rahim = 0     # رحيم (Alif-Lam olmadan)
    
    for surah in data:
        for ayah in surah['verses']:
            text = clean_for_word_count(ayah['text'])
            
            # الرحيم sayımı
            count_al_rahim += text.count('الرحيم')
            
            # رحيم sayımı (ama الرحيم içindeki رحيم'i çift saymamalıyız)
            # Önce الرحيم'i geçici bir işaretle değiştirelim
            temp_text = text.replace('الرحيم', '###MARKED###')
            count_rahim += temp_text.count('رحيم')
    
    print("Rahim Kelimesi Detaylı Analiz:")
    print("="*50)
    print(f"الرحيم (Alif-Lam ile): {count_al_rahim}")
    print(f"رحيم (Alif-Lam olmadan, الرحيم hariç): {count_rahim}")
    print(f"\nToplam: {count_al_rahim + count_rahim}")
    
    # 19 Sistemi Kontrolü
    total = count_al_rahim + count_rahim
    print("\n19 Sistemi Kontrolü:")
    if total % 19 == 0:
        print(f"✅ Rahim Toplam: {total} = 19 x {total // 19}")
    else:
        print(f"❌ Rahim Toplam: {total} (Kalan: {total % 19})")
    
    # Sadece الرحيم kontrolü
    if count_al_rahim % 19 == 0:
        print(f"✅ Sadece الرحيم: {count_al_rahim} = 19 x {count_al_rahim // 19}")
    else:
        print(f"❌ Sadece الرحيم: {count_al_rahim} (Kalan: {count_al_rahim % 19})")
    
    # Sadece رحيم kontrolü
    if count_rahim % 19 == 0:
        print(f"✅ Sadece رحيم: {count_rahim} = 19 x {count_rahim // 19}")
    else:
        print(f"❌ Sadece رحيم: {count_rahim} (Kalan: {count_rahim % 19})")
    
    return count_al_rahim, count_rahim

if __name__ == "__main__":
    analyze_rahim_detailed()
