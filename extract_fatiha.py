"""
Sadece Fatiha suresinin kelime kelime verisini cikarir.
Test icin kucuk bir dosya olusturur.
"""

import json
import sys

# Windows konsol icin UTF-8 encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

print(">> Fatiha suresi kelime kelime verisi cikartiliyor...")

try:
    # Ana dosyayı oku
    with open("quran_word_by_word.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Sadece 1. sureyi bul
    fatiha = None
    for surah in data.get("surahs", []):
        if surah.get("surah_number") == 1:
            fatiha = surah
            break
    
    if fatiha:
        # Sadece Fatiha'yı kaydet
        output = {"surah": fatiha}
        
        with open("words_001.json", 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        # İstatistik
        verse_count = len(fatiha.get("verses", []))
        total_words = sum(len(v.get("words", [])) for v in fatiha.get("verses", []))
        
        print(f"[OK] Basarili!")
        print(f">> Sure: {fatiha.get('surah_name_arabic')} ({fatiha.get('surah_name_english')})")
        print(f">> Ayet sayisi: {verse_count}")
        print(f">> Kelime sayisi: {total_words}")
        print(f">> Dosya: words_001.json")
    else:
        print("[HATA] Fatiha suresi bulunamadi!")

except FileNotFoundError:
    print("[HATA] quran_word_by_word.json dosyasi bulunamadi!")
except Exception as e:
    print(f"[HATA] Hata: {e}")
