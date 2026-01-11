"""
Word-by-Word Veri Yapısını İnceleme
İngilizce kelime kelime meal verisinin bir örneğini çeker.
"""
import requests
import json

def check_wbw_structure():
    print("Word-by-Word verisi kontrol ediliyor...")
    # Fatiha 1. Ayet
    url = "http://api.alquran.cloud/v1/ayah/1:1/editions/quran-wordbyword"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if 'data' in data and len(data['data']) > 0:
            ayah_data = data['data'][0]
            print(f"Baskı: {ayah_data['edition']['name']}")
            print(f"Dil: {ayah_data['edition']['language']}")
            print("-" * 40)
            print("Metin:", ayah_data['text'])
            print("-" * 40)
            print("Ham veri yapısı:")
            print(json.dumps(ayah_data, indent=2))
        else:
            print("Veri bulunamadı.")
            
    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    check_wbw_structure()
