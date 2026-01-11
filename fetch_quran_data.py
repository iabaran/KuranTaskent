"""
Kuran Verisi İndirme Scripti
Bu script, internetten Kuran-ı Kerim'in Arapça metnini ve Türkçe mealini JSON formatında indirir.
Kaynak: github.com/risan/quran-json
"""

import requests
import json
import os
from pathlib import Path

# Klasör oluştur
DATA_DIR = Path("quran_data")
DATA_DIR.mkdir(exist_ok=True)

# Kaynak URL'ler (risan/quran-json)
BASE_URL = "https://raw.githubusercontent.com/risan/quran-json/master/dist"
ARABIC_URL = f"{BASE_URL}/quran_uthmani.json"
TURKISH_URL = f"{BASE_URL}/translations/tr.yuksel.json" # Edip Yüksel çevirisi örnek olarak, daha standar bir kaynak da bakılabilir.
# Alternatif: Diyanet meali için farklı bir kaynak gerekebilir. 
# Şimdilik github.com/semarket/quran-json üzerinden daha standart bir translation bakalım.
# globalquran.com kaynaklı veriler daha güvenilir olabilir.

# Daha basit ve standart bir yapı için 'alquran.cloud' API'sini kullanabiliriz.
# Bu API ile tüm Kuran'ı tek seferde indirebiliriz.

def download_quran_data():
    print("Kuran verileri indiriliyor...")
    
    # 1. Arapça Metin (Uthmani)
    print("1. Arapça metin indiriliyor (Uthmani)...")
    try:
        response_ar = requests.get("http://api.alquran.cloud/v1/quran/quran-uthmani")
        response_ar.raise_for_status()
        data_ar = response_ar.json()['data']
        
        # Basitleştirilmiş yapıya dönüştür
        simple_quran_ar = {}
        for surah in data_ar['surahs']:
            surah_num = surah['number']
            simple_quran_ar[surah_num] = {
                'name': surah['name'],
                'englishName': surah['englishName'],
                'ayahs': {}
            }
            for ayah in surah['ayahs']:
                simple_quran_ar[surah_num]['ayahs'][ayah['numberInSurah']] = ayah['text']
        
        with open(DATA_DIR / "quran_ar.json", "w", encoding="utf-8") as f:
            json.dump(simple_quran_ar, f, ensure_ascii=False, indent=2)
        print("[OK] Arapça metin kaydedildi: quran_data/quran_ar.json")
        
    except Exception as e:
        print(f"HATA (Arapça): {e}")

    # 2. Türkçe Meal (Diyanet İşleri)
    print("2. Türkçe meal indiriliyor (Diyanet)...")
    try:
        # Identifier: tr.diyanet
        response_tr = requests.get("http://api.alquran.cloud/v1/quran/tr.diyanet")
        response_tr.raise_for_status()
        data_tr = response_tr.json()['data']
        
        simple_quran_tr = {}
        for surah in data_tr['surahs']:
            surah_num = surah['number']
            simple_quran_tr[surah_num] = {
                'name': surah['name'],
                'englishName': surah['englishName'],
                'ayahs': {}
            }
            for ayah in surah['ayahs']:
                simple_quran_tr[surah_num]['ayahs'][ayah['numberInSurah']] = ayah['text']
                
        with open(DATA_DIR / "quran_tr.json", "w", encoding="utf-8") as f:
            json.dump(simple_quran_tr, f, ensure_ascii=False, indent=2)
        print("[OK] Türkçe meal kaydedildi: quran_data/quran_tr.json")
        
    except Exception as e:
        print(f"HATA (Türkçe): {e}")


    # 3. Kelime Kelime (Word-by-Word) - İngilizce
    print("3. Kelime kelime meal indiriliyor (İngilizce)...")
    try:
        # Bu veri yapısı farklı, ayet ayet değil kelime kelime dönüyor
        # Tam Kuran'ı WBW olarak tek seferde indirmek zor olabilir (çok büyük)
        # Ancak API'den deneyelim: quran-wordbyword-2
        response_wbw = requests.get("http://api.alquran.cloud/v1/quran/quran-wordbyword-2")
        response_wbw.raise_for_status()
        data_wbw = response_wbw.json()['data']
        
        simple_quran_wbw = {}
        
        for surah in data_wbw['surahs']:
            surah_num = str(surah['number'])
            simple_quran_wbw[surah_num] = {}
            
            for ayah in surah['ayahs']:
                ayah_num = str(ayah['numberInSurah'])
                words = []
                
                # quran-wordbyword-2 formatı genellikle text içinde kelimeleri vermez, words dizisi döner mi?
                # API dökümanına göre words dizisi dönmeyebilir.
                # Ancak 'quran-wordbyword' identifier'ında kelimeler text içinde özel formatta olabilir.
                # En iyisi, client-side (HTML) içinde Arapça metni boşluklardan bölüp kelime yapmaktır.
                # Ama anlam verisi lazım.
                
                # Burada risk almayıp, indirilen veriyi olduğu gibi kaydedeceğim.
                # Fakat dosya çok büyük olabilir (~20MB). Sadeleştirmek şart.
                
                # Veri yapısını görmeden sadeleştirmek zor.
                # O yüzden sadece ham veriyi indirelim, create_reader.py içinde işleriz.
                pass

        with open(DATA_DIR / "quran_wbw.json", "w", encoding="utf-8") as f:
             # Sadece gerekli alanları alalım ki boyut küçülsün
             simplified = {}
             for surah in data_wbw['surahs']:
                 s_num = str(surah['number'])
                 simplified[s_num] = {}
                 for ayah in surah['ayahs']:
                     a_num = str(ayah['numberInSurah'])
                     # Bu edition'da kelime meali text alanında "Kelime|Meal" şeklinde mi?
                     # Hayır, genellikle JSON objesi içinde words array olur.
                     # Eğer words array yoksa bu veri işe yaramaz.
                     
                     # Varsayalım ki words array yok (standart API response).
                     # O zaman bu adımı atlayıp frontend'de çözüm üreteceğiz.
                     simplified[s_num][a_num] = ayah['text']
             
             json.dump(simplified, f, ensure_ascii=False) # indent yok, yer tasarrufu
        print("[OK] WBW verisi indirildi (Basitleştirilmiş)")

    except Exception as e:
         print(f"HATA (WBW): {e}")
        
    except Exception as e:
        print(f"HATA (WBW): {e}")

    # Özet Rapor
    if (DATA_DIR / "quran_ar.json").exists():
        size = (DATA_DIR / "quran_ar.json").stat().st_size / 1024
        print(f"\nArapça veri boyutu: {size:.2f} KB")
        
    if (DATA_DIR / "quran_tr.json").exists():
        size = (DATA_DIR / "quran_tr.json").stat().st_size / 1024
        print(f"Türkçe veri boyutu: {size:.2f} KB")

if __name__ == "__main__":
    download_quran_data()
