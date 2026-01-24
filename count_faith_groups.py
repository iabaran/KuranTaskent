import re
import json
import sys

# Dosya yolları
QURAN_FILE = "d:\\KuranTaskent\\quran_arabic.json"
OUTPUT_JS_FILE = "d:\\KuranTaskent\\faith_groups_data.js"

# Arapça Harekeleri Temizleme ve Normalizasyon Fonksiyonu
def normalize_arabic(text):
    # 1. Superscript Alef (0670) -> Normal Alef (0627) yap
    # Çünkü Kur'an imlasında 'Kitab', 'Rahman', 'Munafik' gibi kelimelerde uzatma Elif'i asar olarak yazılır.
    text = re.sub(r'\u0670', 'ا', text)
    
    # 2. Harekeleri ve diğer özel işaretleri kaldır
    # 0610-061A: Honorifics etc
    # 064B-065F: Harekeler
    # 06D6-06ED: Quranic marks (Small High Ligatures etc.)
    text = re.sub(r'[\u0610-\u061A\u064B-\u065F\u06D6-\u06ED]', '', text)
    
    # 3. Alef varyasyonlarını normalleştir (أ, إ, آ, ٱ -> ا)
    text = re.sub(r'[أإآٱ]', 'ا', text)
    
    return text

# Hedef Kelimeler ve Regex Desenleri (Harekesiz ve Normalize edilmiş metin için)
def create_regex(core_pattern):
    prefix = r"(?:[وفلبك]?(?:ال)?)"
    suffix = r"(?:ون|ين|ات|ان|ة)?" 
    return re.compile(r"\b" + prefix + core_pattern + suffix + r"\b")

patterns = {
    "Munafik": create_regex(r"من[ا]?فق"), # Alef opsiyonel (منفق veya منافق)
    "Mushrik": create_regex(r"مشرك"),
    "Muslim": create_regex(r"مسلم"),
    "Mumin": create_regex(r"م[وؤ]?من"), # Waw/Hamza opsiyonel
    "Nasara": create_regex(r"نص[ا]?ر[ىي]"), # Alef opsiyonel, son harf Y/AlefMaksura
    "Yahud": re.compile(r"\b(?:[وفلبك]?(?:ال)?)?(?:يهود|هادوا)\b")
}

# Sonuçları saklayacak yapı
results = {key: {"count": 0, "locations": []} for key in patterns}

def main():
    print("Kur'an JSON dosyası taranıyor...")
    
    try:
        with open(QURAN_FILE, 'r', encoding='utf-8') as f:
            quran_data = json.load(f)
            
        for surah in quran_data:
            surah_num = surah["id"]
            for verse in surah["verses"]:
                ayah_num = verse["id"]
                original_text = verse["text"]
                
                # Harekeleri temizle ve normalize et
                clean_text = normalize_arabic(original_text)
                
                # Her kategori için kontrol et
                for key, pattern in patterns.items():
                    matches = pattern.findall(clean_text)
                    if matches:
                        count = len(matches)
                        # Özel kontrol: Ali-Imran 52 (Nasara)
                        # Eğer çok fazla veya az çıkarsa burada debug yapılabilir.
                        
                        results[key]["count"] += count
                        results[key]["locations"].append({
                            "s": surah_num,
                            "a": ayah_num,
                            "count": count,
                            "text": original_text 
                        })
                    
        # Sonuçları yazdır
        print("-" * 30)
        for key, data in results.items():
            print(f"{key}: {data['count']}")
        print("-" * 30)
        
        # JS dosyasına kaydet
        js_content = "const faithGroupsData = " + json.dumps(results, ensure_ascii=False, indent=4) + ";"
        with open(OUTPUT_JS_FILE, 'w', encoding='utf-8') as f:
            f.write(js_content)
            
        print(f"Veriler '{OUTPUT_JS_FILE}' dosyasına kaydedildi.")
        
    except Exception as e:
        print(f"Hata oluştu: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
