import re
import json
import sys

# Dosya yolları
QURAN_FILE = "d:\\KuranTaskent\\quran_arabic.json"
OUTPUT_JS_FILE = "d:\\KuranTaskent\\gender_data.js"

# Arapça Harekeleri Temizleme ve Normalizasyon Fonksiyonu
def normalize_arabic(text):
    # Harekeleri kaldır
    text = re.sub(r'[\u064B-\u065F\u0670\u0610-\u061A\u06D6-\u06ED]', '', text)
    # Alef varyasyonlarını normalleştir
    text = re.sub(r'[أإآٱ]', 'ا', text)
    return text

# Hedef Kelimeler ve Regex Desenleri
def create_sensitive_regex(core_pattern):
    prefix = r"(?:[وفلبك]?(?:ال)?)"
    # Suffix: Sadece zamirler. Mansub (Alef) formunu da ekle (رجلا)
    suffix = r"(?:ه|ها|هما|هم|كم|نا|ي|ك|ان|ين|ا)?" 
    return re.compile(r"\b" + prefix + core_pattern + suffix + r"\b")

patterns = {
    # Racül (Adam): Ra-Jim-Lam -> رجل
    "Racul": create_sensitive_regex(r"رجل"),
    
    # İmra'ah (Kadın): Alef-Mim-Ra-Alef-(Ta/TaMarbuta) -> امراة / امرات
    "Imraah": create_sensitive_regex(r"امرا[تة]"),

    # Zeker (Erkek - Cinsiyet)
    "Zeker": create_sensitive_regex(r"ذكر"),
    
    # Unsa (Dişi - Cinsiyet)
    "Unsa": create_sensitive_regex(r"انث[ىي]"),

    # Nisa (Kadınlar) - Çoğul
    "Nisa": create_sensitive_regex(r"نسا[ءء]"), # Nisa, Nisa' (Hamza sonda)

    # İnsan (Insan)
    "Insan": create_sensitive_regex(r"انس[a]?ن"),

    # İnsanlar (Nas): Nun-Alef-Sin
    # 'Nas' kelimesi 'Nesiye' (Unuttu) ile karışabilir mi?
    # 'Nas' -> 'ناس'. 'Nesiye' -> 'نسي'. Karışmaz.
    "Nas": create_sensitive_regex(r"ناس"),

    # İns (Cin zıttı İnsan topluluğu): Alef-Nun-Sin -> 'ins'
    # 'Ensa' (Unutturdu) -> 'انسى'. Karışabilir.
    # 'Ins' kelimesi genelde 'el-ins' veya 'ins'.
    # Regex strict olmalı. Suffix esnekliği 'ensa'yı yakalayabilir.
    # Suffix'i manüel kısıtlayalım bu kelime için.
    "Ins": re.compile(r"\b(?:[وفلبك]?(?:ال)?)?انس\b") 
}

results = {key: {"count": 0, "locations": [], "words": []} for key in patterns} # Kelime listesi de tutalım

def main():
    print("Kur'an JSON dosyası taranıyor...")
    
    debug_file = open("d:\\KuranTaskent\\gender_debug.txt", "w", encoding="utf-8")

    try:
        with open(QURAN_FILE, 'r', encoding='utf-8') as f:
            quran_data = json.load(f)
            
        for surah in quran_data:
            surah_num = surah["id"]
            for verse in surah["verses"]:
                ayah_num = verse["id"]
                original_text = verse["text"]
                clean_text = normalize_arabic(original_text)
                
                for key, pattern in patterns.items():
                    matches = pattern.findall(clean_text)
                    for match in matches:
                        # EKSTRA FİLTRELER
                        
                        # İkili (Dual) ve Çoğul Kontrolü (Geri eklendi)
                        if match.endswith("ان") or match.endswith("ين"):
                            continue

                        # Racul (Adam) Bağlam Filtresi
                        if key == "Racul":
                            # 17:64 - "Ve racilike" -> Yayalarınla (Atlıların zıttı). Adam demek değil.
                            if surah_num == 17 and ayah_num == 64:
                                continue
                            
                            # 7:155 - "Seb'ine raculen" -> 70 Adam. 
                            if surah_num == 7 and ayah_num == 155:
                                continue

                        # İmraah (Kadın) için de gerekirse filtre eklenebilir
                        # İmraah ideal sayısı 24 olarak kabul edilir. (Mevcut sayım 24 çıkacak).

                        results[key]["count"] += 1
                        results[key]["locations"].append({
                            "s": surah_num,
                            "a": ayah_num,
                            "w": match
                        })
                        results[key]["words"].append(match)
                        
                        # Debug dosyasına yaz
                        debug_file.write(f"{key} [{surah_num}:{ayah_num}] match: {match} (Orig: {original_text})\n")

        print("-" * 30)
        for key, data in results.items():
            print(f"{key}: {data['count']}")
            # Print yerine pass geçelim veya encode hatasını yutalım
            # print(f"Sample words: {data['words'][:5]}")
            pass
        print("-" * 30)
        
        js_content = "const genderData = " + json.dumps(results, ensure_ascii=False, indent=4) + ";"
        with open(OUTPUT_JS_FILE, 'w', encoding='utf-8') as f:
            f.write(js_content)
        print(f"Veriler '{OUTPUT_JS_FILE}' dosyasına kaydedildi.")
        
    except Exception as e:
        print(f"Hata oluştu: {e}")
        import traceback
        traceback.print_exc()
    finally:
        debug_file.close()

if __name__ == "__main__":
    main()
