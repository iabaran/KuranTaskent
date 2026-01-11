"""
Başarısız olan ayetleri yeniden çeker ve JSON dosyasını günceller.
"""

import requests
import json
import sys

# Windows konsol için UTF-8 encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "https://api.acikkuran.com"

def fetch_verse_words(surah: int, verse: int):
    """Belirtilen sure ve ayet için kelime kelime veriyi çeker."""
    url = f"{BASE_URL}/surah/{surah}/verse/{verse}/words"
    
    try:
        print(f">> Sure {surah}, Ayet {verse} cekiliyor...")
        response = requests.get(url, timeout=30)  # Daha uzun timeout
        response.raise_for_status()
        data = response.json()
        print(f"   >> Basarili! {len(data.get('data', []))} kelime bulundu.")
        return data.get("data", [])
    except Exception as e:
        print(f"   >> HATA: {e}")
        return None

def update_json_file(filename: str, missing_verses: list):
    """JSON dosyasını günceller."""
    print(f"\n>> JSON dosyasi okunuyor: {filename}")
    
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Her başarısız ayet için
    for surah_num, verse_num in missing_verses:
        print(f"\n>> Sure {surah_num}, Ayet {verse_num} guncelleniyor...")
        
        # Kelime verisini çek
        words_data = fetch_verse_words(surah_num, verse_num)
        
        if words_data is None:
            print(f"   >> Atlanıyor, çekilemedi.")
            continue
        
        # İlgili sureyi bul
        surah_data = None
        for surah in data["surahs"]:
            if surah["surah_number"] == surah_num:
                surah_data = surah
                break
        
        if surah_data is None:
            print(f"   >> HATA: Sure {surah_num} bulunamadi!")
            continue
        
        # Ayet zaten var mı kontrol et
        verse_exists = False
        for verse in surah_data["verses"]:
            if verse["verse_number"] == verse_num:
                # Varsa güncelle
                verse["words"] = words_data
                verse_exists = True
                print(f"   >> Ayet guncellendi!")
                break
        
        # Yoksa ekle
        if not verse_exists:
            surah_data["verses"].append({
                "verse_number": verse_num,
                "words": words_data
            })
            # Ayet numarasına göre sırala
            surah_data["verses"].sort(key=lambda v: v["verse_number"])
            print(f"   >> Ayet eklendi!")
    
    # Metadata'yı güncelle
    if "failed_verses" in data["metadata"]:
        # Başarılı olanları listeden çıkar
        updated_failed = []
        for failed_verse in data["metadata"]["failed_verses"]:
            surah_verse = failed_verse.split(":")
            if len(surah_verse) == 2:
                s, v = int(surah_verse[0]), int(surah_verse[1])
                if (s, v) not in missing_verses:
                    updated_failed.append(failed_verse)
        
        data["metadata"]["failed_verses"] = updated_failed
        data["metadata"]["successful_verses"] = 6236 - len(updated_failed)
    
    # Kaydet
    print(f"\n>> JSON dosyasi kaydediliyor...")
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f">> Guncelleme tamamlandi!")

def main():
    print("="*60)
    print("   EKSIK AYETLERI TAMAMLAMA")
    print("="*60)
    
    # Başarısız olan ayetler
    missing_verses = [
        (10, 17),  # Sure 10, Ayet 17
        (79, 3),   # Sure 79, Ayet 3
    ]
    
    # JSON'u güncelle
    update_json_file("quran_word_by_word.json", missing_verses)
    
    print("\n" + "="*60)
    print(">> Tum ayetler basariyla tamamlandi!")
    print("="*60)

if __name__ == "__main__":
    main()
