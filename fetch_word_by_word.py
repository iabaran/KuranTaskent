"""
Açık Kuran API - Kelime Kelime Veri Çekme
Bu script tüm Kur'an için kelime kelime Türkçe çeviri ve kök bilgilerini çeker.
"""

import requests
import json
import time
import sys
from typing import Dict, List, Optional

# Windows konsol için UTF-8 encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Kur'an'daki sure ve ayet sayıları
SURAH_VERSE_COUNTS = [
    7, 286, 200, 176, 120, 165, 206, 75, 129, 109, 123, 111, 43, 52, 99,
    128, 111, 110, 98, 135, 112, 78, 118, 64, 77, 227, 93, 88, 69, 60,
    34, 30, 73, 54, 45, 83, 182, 88, 75, 85, 54, 53, 89, 59, 37, 35,
    38, 29, 18, 45, 60, 49, 62, 55, 78, 96, 29, 22, 24, 13, 14, 11,
    11, 18, 12, 12, 30, 52, 52, 44, 28, 28, 20, 56, 40, 31, 50, 40,
    46, 42, 29, 19, 36, 25, 22, 17, 19, 26, 30, 20, 15, 21, 11, 8,
    8, 19, 5, 8, 8, 11, 11, 8, 3, 9, 5, 4, 7, 3, 6, 3, 5, 4, 5, 6
]

BASE_URL = "https://api.acikkuran.com"

def fetch_verse_words(surah: int, verse: int) -> Optional[List[Dict]]:
    """
    Belirtilen sure ve ayet için kelime kelime veriyi çeker.
    
    Args:
        surah: Sure numarası (1-114)
        verse: Ayet numarası
        
    Returns:
        Kelime listesi veya None (hata durumunda)
    """
    url = f"{BASE_URL}/surah/{surah}/verse/{verse}/words"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("data", [])
    except requests.exceptions.RequestException as e:
        print(f"[HATA] Sure {surah}, Ayet {verse} - {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"[JSON HATASI] Sure {surah}, Ayet {verse} - {e}")
        return None

def fetch_all_word_by_word_data() -> Dict:
    """
    Tüm Kur'an için kelime kelime veriyi çeker.
    
    Returns:
        Tüm veriyi içeren dictionary
    """
    print(">> Açık Kuran API'den kelime kelime veriler çekiliyor...\n")
    
    all_data = {
        "metadata": {
            "source": "Açık Kuran API",
            "url": "https://api.acikkuran.com",
            "total_surahs": 114,
            "total_verses": sum(SURAH_VERSE_COUNTS)
        },
        "surahs": []
    }
    
    total_verses = 0
    successful_verses = 0
    failed_verses = []
    
    for surah_num in range(1, 115):  # 114 sure
        verse_count = SURAH_VERSE_COUNTS[surah_num - 1]
        
        surah_data = {
            "surah_number": surah_num,
            "verse_count": verse_count,
            "verses": []
        }
        
        print(f"[Sure {surah_num}/{114} - {verse_count} ayet]", end=" ")
        
        for verse_num in range(1, verse_count + 1):
            total_verses += 1
            
            words_data = fetch_verse_words(surah_num, verse_num)
            
            if words_data is not None:
                surah_data["verses"].append({
                    "verse_number": verse_num,
                    "words": words_data
                })
                successful_verses += 1
            else:
                failed_verses.append(f"{surah_num}:{verse_num}")
            
            # API'yi yormamak için kısa bekleme
            time.sleep(0.1)
        
        all_data["surahs"].append(surah_data)
        print(f"OK")
    
    # Özet istatistikler
    print(f"\n" + "="*60)
    print(f"OZET:")
    print(f"   Toplam Ayet: {total_verses}")
    print(f"   Basarili: {successful_verses}")
    print(f"   Basarisiz: {len(failed_verses)}")
    
    if failed_verses:
        print(f"\n[UYARI] Basarisiz ayetler: {', '.join(failed_verses)}")
    
    all_data["metadata"]["successful_verses"] = successful_verses
    all_data["metadata"]["failed_verses"] = failed_verses
    
    return all_data

def save_data(data: Dict, filename: str = "quran_word_by_word.json"):
    """
    Veriyi JSON dosyasına kaydeder.
    
    Args:
        data: Kaydedilecek veri
        filename: Dosya adı
    """
    print(f"\n>> Veri kaydediliyor: {filename}")
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f">> Kayit tamamlandi!")

def main():
    """Ana fonksiyon"""
    print("="*60)
    print("   ACIK KURAN - KELIME KELIME VERI CEKME")
    print("="*60)
    print()
    
    # Veriyi çek
    all_data = fetch_all_word_by_word_data()
    
    # Kaydet
    save_data(all_data)
    
    print("\n" + "="*60)
    print(">> Islem tamamlandi!")
    print("="*60)

if __name__ == "__main__":
    main()
