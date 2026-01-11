"""
API Seçeneklerini Kontrol Etme
alquran.cloud üzerindeki 'wordbyword' ve Türkçe kaynakları listeler.
"""

import requests
import json

def check_editions():
    print("API seçenekleri kontrol ediliyor...")
    
    try:
        response = requests.get("http://api.alquran.cloud/v1/edition?format=json")
        data = response.json()['data']
        
        wbw_editions = []
        turkish_editions = []
        
        # Veri yapısını güvenli bir şekilde işle
        if isinstance(data, list):
            for e in data:
                try:
                    fmt = e.get('format', '')
                    lang = e.get('language', '')
                    etype = e.get('type', '')
                    ident = e.get('identifier', '')
                    name = e.get('name', '')
                    
                    if 'word' in etype.lower():
                        wbw_editions.append(f"{ident}: {name} ({lang})")
                    
                    if lang == 'tr':
                        turkish_editions.append(f"{ident}: {name} ({etype})")
                except:
                    pass
        
        print(f"\nWord-by-Word Seçenekleri ({len(wbw_editions)} adet):")
        for e in wbw_editions:
            print(f"- {e}")
            
        print(f"\nTürkçe Seçenekleri ({len(turkish_editions)} adet):")
        for e in turkish_editions:
            print(f"- {e}")
            
    except Exception as e:
        print(f"Hata: {e}")
        # Hata durumunda yapıyı anlamak için ilk elemanı yazdır
        if 'data' in locals() and isinstance(data, list) and len(data) > 0:
            print("Örnek veri yapısı:", data[0])

if __name__ == "__main__":
    check_editions()
