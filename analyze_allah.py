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

def analyze_allah_forms():
    """Allah lafzının tüm formlarını analiz et"""
    if not os.path.exists(ARABIC_DATA_PATH):
        print("Arabic data file not found!")
        return

    with open(ARABIC_DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Allah'ın olası tüm formları
    allah_forms = {
        'الله': 0,      # Standart form
        'لله': 0,       # Lam ile (lillah)
        'بالله': 0,     # Ba ile (billah)
        'والله': 0,     # Vav ile (wallah)
        'فالله': 0,     # Fa ile (fallah)
        'تالله': 0,     # Ta ile (tallah)
        'اللهم': 0,     # Allahumme (genelde hariç tutulur)
    }
    
    for surah in data:
        for ayah in surah['verses']:
            text = clean_for_word_count(ayah['text'])
            
            for form in allah_forms:
                allah_forms[form] += text.count(form)
    
    print("Allah Lafzı Form Analizi:")
    print("="*50)
    for form, count in allah_forms.items():
        print(f"{form}: {count}")
    
    # Allahumme hariç toplam
    total_without_allahumme = sum(allah_forms.values()) - allah_forms['اللهم']
    print(f"\nToplam (Allahumme hariç): {total_without_allahumme}")
    print(f"Toplam (Allahumme dahil): {sum(allah_forms.values())}")
    
    # 19 Sistemi Kontrolü
    print("\n19 Sistemi Kontrolü:")
    if total_without_allahumme % 19 == 0:
        print(f"✅ Allah (Allahumme hariç): {total_without_allahumme} = 19 x {total_without_allahumme // 19}")
    else:
        print(f"❌ Allah (Allahumme hariç): {total_without_allahumme} (Kalan: {total_without_allahumme % 19})")
    
    return allah_forms

if __name__ == "__main__":
    analyze_allah_forms()
