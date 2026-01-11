"""
Kelime kelime Kur'an verisini doğrular.
"""

import json
import sys

# Windows konsol için UTF-8 encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Sure ve ayet sayıları
SURAH_VERSE_COUNTS = [
    7, 286, 200, 176, 120, 165, 206, 75, 129, 109, 123, 111, 43, 52, 99,
    128, 111, 110, 98, 135, 112, 78, 118, 64, 77, 227, 93, 88, 69, 60,
    34, 30, 73, 54, 45, 83, 182, 88, 75, 85, 54, 53, 89, 59, 37, 35,
    38, 29, 18, 45, 60, 49, 62, 55, 78, 96, 29, 22, 24, 13, 14, 11,
    11, 18, 12, 12, 30, 52, 52, 44, 28, 28, 20, 56, 40, 31, 50, 40,
    46, 42, 29, 19, 36, 25, 22, 17, 19, 26, 30, 20, 15, 21, 11, 8,
    8, 19, 5, 8, 8, 11, 11, 8, 3, 9, 5, 4, 7, 3, 6, 3, 5, 4, 5, 6
]

def verify_data():
    """JSON dosyasını doğrular."""
    print("="*60)
    print("   KELIME KELIME KURAN VERISI DOGRULAMA")
    print("="*60)
    print()
    
    # JSON'u oku
    print(">> JSON dosyasi okunuyor...")
    with open("quran_word_by_word.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(">> OK\n")
    
    # İstatistikler
    total_verses = 0
    total_words = 0
    missing_verses = []
    
    # Her sureyi kontrol et
    print(">> Sureler kontrol ediliyor...\n")
    for surah_num in range(1, 115):
        expected_verses = SURAH_VERSE_COUNTS[surah_num - 1]
        
        # Sureyi bul
        surah_data = None
        for surah in data["surahs"]:
            if surah["surah_number"] == surah_num:
                surah_data = surah
                break
        
        if surah_data is None:
            print(f"[HATA] Sure {surah_num} bulunamadi!")
            continue
        
        # Ayetleri kontrol et
        verse_numbers = [v["verse_number"] for v in surah_data["verses"]]
        
        for verse_num in range(1, expected_verses + 1):
            total_verses += 1
            
            if verse_num not in verse_numbers:
                missing_verses.append(f"{surah_num}:{verse_num}")
            else:
                # Kelime sayısını say
                for verse in surah_data["verses"]:
                    if verse["verse_number"] == verse_num:
                        total_words += len(verse.get("words", []))
                        break
        
        print(f"   Sure {surah_num:3d}/114 - {len(verse_numbers):3d}/{expected_verses:3d} ayet {'OK' if len(verse_numbers) == expected_verses else 'EKSIK'}")
    
    # Sonuçlar
    print("\n" + "="*60)
    print("SONUCLAR:")
    print("="*60)
    print(f"Toplam Sure      : 114")
    print(f"Toplam Ayet      : {total_verses}")
    print(f"Eksik Ayet       : {len(missing_verses)}")
    print(f"Basarili Ayet    : {total_verses - len(missing_verses)}")
    print(f"Toplam Kelime    : {total_words:,}")
    print("="*60)
    
    if missing_verses:
        print(f"\n[UYARI] Eksik ayetler: {', '.join(missing_verses)}")
        print("="*60)
    else:
        print("\n>> TUM AYETLER TAMAMLANDI!")
        print(">> Veri seti %100 eksiksiz!")
        print("="*60)

if __name__ == "__main__":
    verify_data()
