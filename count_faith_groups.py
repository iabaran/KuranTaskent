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

# Hedef Kelimeler ve Regex Desenleri (Kök tabanlı esnek arama)
def create_sensitive_regex(pattern):
    # Prefix: Wa, Fa, Lam, Ba, Kaf, Al
    prefix = r"(?:[وفلبك]?(?:ال)?)"
    # Suffix: wn, yn, at, an, a (tekil dişil), hum, him vb
    suffix = r"(?:ون|ين|ات|ان|ة|هم|كم)?" 
    return re.compile(r"\b" + prefix + pattern + suffix + r"\b")

patterns = {
    # Munafik: Mim-Nun-(Alef?)-Fa-Qaf
    "Munafik": create_sensitive_regex(r"من[ا]?فق"),
    
    # Mushrik: Mim-Shin-Ra-Kaf
    "Mushrik": create_sensitive_regex(r"مشرك"),
    
    # Muslim: Mim-Sin-Lam-Mim
    "Muslim": create_sensitive_regex(r"مسلم"),
    
    # Mumin: Mim-(Waw/Hamza/Alef?)-Mim-Nun
    # 'Mu'min' bazen 'مؤمن', bazen 'مومن' (temizlenince)
    "Mumin": create_sensitive_regex(r"م[وؤأا]?من"),
    
    # Nasara: Nun-Sad-(Alef?)-Ra-(Ya/Alef/Maksura?)-(Alef?)
    # Nasara, Nasra, Nasraniyy
    # Hıristiyan: النصارى, نصرانيا
    "Nasara": create_sensitive_regex(r"نص[ا]?ر(?:[ايىي]|$)[ا]?"),
    
    # Yahud: Ya-Ha-(Waw?)-Dal- ... 
    # Yahud, Hud, Haadu (Alladhina Hadu için ayrı bir mantık lazım ama kelime olarak Hadu da sayılabilir mi?)
    # Yahudi: اليهود
    # Alladhina Hadu: الذين هادوا (Bu iki kelime, regex ile zorlayabiliriz veya metin içinde ararız)
    # Şimdilik "Yahud" (يهود) ve "Hud" (هود - ama Hud peygamber ile karışabilir!)
    # Hud Peygamber ile karışmaması için dikkatli olunmalı. Hud (AS) ismi 'هود' olarak geçer.
    # Yahudiler için 'هدنا', 'هادوا', 'يهود' kullanılır.
    # En güvenlisi 'al-Yahud' (اليهود) ve 'Hadu' (هادوا).
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
