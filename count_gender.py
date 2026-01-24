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
    "Unsa": create_sensitive_regex(r"انث[ىي]")
}

results = {key: {"count": 0, "locations": [], "words": []} for key in patterns} # Kelime listesi de tutalım

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
                clean_text = normalize_arabic(original_text)
                
                for key, pattern in patterns.items():
                    matches = pattern.findall(clean_text)
                    for match in matches:
                        # EKSTRA FİLTRELER
                        
                        # İkili (Dual) ve Çoğul Kontrolü
                        # Racul-an (İki adam), Racul-ayn (İki adam)
                        # Imraat-an (İki kadın), Imraat-ayn
                        # Zeker (Cinsiyet)
                        
                        # Eğer match sonu 'ان' (an) veya 'ين' (yn) ile bitiyorsa bu ikilidir (Dual).
                        # istisna: Bazı kelimelerin kökünde olabilir ama Racul ve Imraah için suffix bu.
                        if match.endswith("ان") or match.endswith("ين"):
                            # Bu bir ikilidir, tekil sayımına dahil etme (veya ayrı say)
                            # 19 mucizesi tekilleri sayar.
                            continue
                            
                        # Racul (Adam) için özel:
                        # Eğer 'ون' (un) veya 'ين' (in) ile bitiyorsa çoğul olabilir mi?
                        # Rical (Adamlar) kırık çoğuldur, suffix almaz. Regex zaten Ricali yakalamaz.
                        # Ama düzenli çoğul olursa? Raculun -> Raculune? Yok.
                        
                        # Zeker (Erkek) -> Zekera (Fiil) ile karışır mı?
                        # Zeker (isim) genelde 'Zeker' veya 'Ez-Zeker'.
                        # Zikr (Öğüt) -> 'Zikr'.
                        # Regex 'Zeker' (zkr) yakalıyor.
                        # Eğer match 'zkr' ise: Bu 'Zikr' mi 'Zeker' mi?
                        # Ayrım metin içi bağlamla olur. Zor.
                        
                        results[key]["count"] += 1
                        results[key]["locations"].append({
                            "s": surah_num,
                            "a": ayah_num,
                            "w": match
                        })
                        results[key]["words"].append(match)

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

if __name__ == "__main__":
    main()
