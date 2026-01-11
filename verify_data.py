"""
Veri Doğrulama Scripti
İndirilen Kuran JSON verilerindeki Sure ve Ayet sayılarını kontrol eder.
"""

import json
from pathlib import Path

DATA_DIR = Path("quran_data")

def verify_data():
    print("Veri doğrulama başlıyor...")
    print("=" * 60)
    
    # Beklenen değerler
    EXPECTED_SURAHS = 114
    EXPECTED_AYAHS = 6236
    
    files = {
        "Arapça": "quran_ar.json",
        "Türkçe": "quran_tr.json"
    }
    
    for label, filename in files.items():
        file_path = DATA_DIR / filename
        
        if not file_path.exists():
            print(f"HATA: {filename} bulunamadı!")
            continue
            
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        surah_count = len(data)
        ayah_count = sum(len(surah['ayahs']) for surah in data.values())
        
        print(f"Dosya: {filename} ({label})")
        print(f"  - Sure Sayısı: {surah_count} (Beklenen: {EXPECTED_SURAHS}) -> {'[OK]' if surah_count == EXPECTED_SURAHS else '[HATA]'}")
        print(f"  - Ayet Sayısı: {ayah_count} (Beklenen: {EXPECTED_AYAHS}) -> {'[OK]' if ayah_count == EXPECTED_AYAHS else '[HATA]'}")
        
        # Örnek Ayet (Fatiha 1)
        if '1' in data:
            fatiha_1 = data['1']['ayahs']['1']
            print(f"  - Örnek (Fatiha 1): {fatiha_1}")
        print("-" * 60)

if __name__ == "__main__":
    verify_data()
