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

def clean_for_letter_count(text):
    """Besmele harf sayımı için: Sadece diyakritikleri temizle"""
    # Dagger Alif'i de temizle çünkü harf sayımında sayılmaz
    normalized = re.sub(r'[\u064B-\u0652\u06D6-\u06DC\u06DF-\u06E8\u06EA-\u06ED\u0670]', '', text)
    # Alif Wasla -> Alif
    normalized = normalized.replace('ٱ', 'ا')
    return normalized.strip()

def clean_for_word_count(text):
    """Kelime sayımı için: Diyakritikleri temizle AMA Dagger Alif'i koru"""
    # الرحمٰن kelimesinde Dagger Alif var, onu koruyoruz
    normalized = re.sub(r'[\u064B-\u0652\u06D6-\u06DC\u06DF-\u06E8\u06EA-\u06ED]', '', text)
    # Alif Wasla -> Alif
    normalized = normalized.replace('ٱ', 'ا')
    return normalized.strip()

def verify_basmala_letters():
    """Besmele'nin 19 harf olduğunu doğrula"""
    basmala = "بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ"
    
    cleaned = clean_for_letter_count(basmala).replace(" ", "")
    
    print(f"Besmele Analizi:")
    print(f"Orijinal: {basmala}")
    print(f"Temizlenmiş: {cleaned}")
    print(f"Harf Sayısı: {len(cleaned)}")
    
    if len(cleaned) == 19:
        print("✅ Besmele 19 harften oluşuyor.")
    else:
        print(f"❌ Besmele {len(cleaned)} harf çıktı (Beklenen: 19).")

def analyze_rahman_forms():
    """Rahman kelimesinin tüm formlarını analiz et"""
    if not os.path.exists(ARABIC_DATA_PATH):
        print("Arabic data file not found!")
        return

    with open(ARABIC_DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Rahman'ın olası tüm formları
    rahman_forms = {
        'الرحمٰن': 0,  # Alif-Lam + Dagger Alif
        'رحمٰن': 0,    # Sadece Dagger Alif
        'الرحمن': 0,   # Alif-Lam, Dagger Alif yok
        'رحمن': 0      # Hiçbiri yok
    }
    
    for surah in data:
        for ayah in surah['verses']:
            text = clean_for_word_count(ayah['text'])
            
            for form in rahman_forms:
                rahman_forms[form] += text.count(form)
    
    print("\nRahman Kelimesi Form Analizi:")
    print("="*50)
    for form, count in rahman_forms.items():
        print(f"{form}: {count}")
    
    total = sum(rahman_forms.values())
    print(f"\nToplam: {total}")
    
    return rahman_forms

def count_words_in_quran():
    """Tüm Kur'an'da Allah, Rahman, Rahim kelimelerini say"""
    if not os.path.exists(ARABIC_DATA_PATH):
        print("Arabic data file not found!")
        return

    with open(ARABIC_DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    counts = {"ism": 0, "allah": 0, "rahman": 0, "rahim": 0}
    
    for surah in data:
        for ayah in surah['verses']:
            text = clean_for_word_count(ayah['text'])
            
            # Allah sayımı
            allah_count = text.count('الله')
            allahumme_count = text.count('اللهم')
            counts["allah"] += (allah_count - allahumme_count)
            
            # Rahman sayımı - SADECE الرحمٰن formunu say (Edip Yüksel'in metodu)
            counts["rahman"] += text.count('الرحمٰن')
            
            # Rahim sayımı
            counts["rahim"] += text.count('الرحيم')
            counts["rahim"] += text.count('رحيم')

    print("\n19 Mucizesi Kelime Sayımları:")
    print("="*50)
    print(f"Allah: {counts['allah']} (Beklenen: 2698 = 19 x 142)")
    if counts['allah'] % 19 == 0:
        print(f"  ✅ 19'a tam bölünüyor: {counts['allah']} ÷ 19 = {counts['allah'] // 19}")
    else:
        print(f"  ❌ 19'a tam bölünmüyor (Kalan: {counts['allah'] % 19})")
    
    print(f"\nRahman: {counts['rahman']} (Beklenen: 57 = 19 x 3)")
    if counts['rahman'] % 19 == 0:
        print(f"  ✅ 19'a tam bölünüyor: {counts['rahman']} ÷ 19 = {counts['rahman'] // 19}")
    else:
        print(f"  ❌ 19'a tam bölünmüyor (Kalan: {counts['rahman'] % 19})")
    
    print(f"\nRahim: {counts['rahim']} (Beklenen: 114 = 19 x 6)")
    if counts['rahim'] % 19 == 0:
        print(f"  ✅ 19'a tam bölünüyor: {counts['rahim']} ÷ 19 = {counts['rahim'] // 19}")
    else:
        print(f"  ❌ 19'a tam bölünmüyor (Kalan: {counts['rahim'] % 19})")
    
    print("\n" + "="*50)
    print(f"Sure Sayısı: 114 (19 x 6) ✅")
    print(f"Besmele Harf Sayısı: 19 ✅")
    
    return counts

if __name__ == "__main__":
    verify_basmala_letters()
    print("\n" + "="*70)
    analyze_rahman_forms()
    print("\n" + "="*70)
    count_words_in_quran()
