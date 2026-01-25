import json
import re

def normalize_arabic(text):
    # Harekeleri kaldır
    text = re.sub(r'[\u064B-\u065F\u0670\u0610-\u061A\u06D6-\u06ED]', '', text)
    # Alef varyasyonlarını normalleştir
    text = re.sub(r'[أإآٱ]', 'ا', text)
    return text

def main():
    file_path = "d:\\KuranTaskent\\quran_arabic.json"
    
    # Aranacak kelimeler (Normalleştirilmiş halleri)
    # Himar (حمار) -> حمار
    # Hamir (حمير) -> حمير
    # Humur (حمر) -> حمر
    
    # Regex kökleri (suffix ve prefix esnekliği ile)
    patterns = {
        "Himar (Tekil)": re.compile(r"\b(?:[وفلبك]?(?:ال)?)?حمار(?:ه|ها|هما|هم|كم|نا|ي|ك)?\b"),
        "Hamir (Çoğul)": re.compile(r"\b(?:[وفلبك]?(?:ال)?)?حمير(?:ه|ها|هما|هم|كم|نا|ي|ك)?\b"),
        "Humur (Yaban)": re.compile(r"\b(?:[وفلبك]?(?:ال)?)?حمر(?:ه|ها|هما|هم|كم|نا|ي|ك)?\b")
    }

    results = {key: [] for key in patterns}

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            quran_data = json.load(f)

        print(f"Toplam {len(quran_data)} sure taranıyor...\n")
        
        for surah in quran_data:
            surah_num = surah["id"]
            for verse in surah["verses"]:
                ayah_num = verse["id"]
                text = verse["text"]
                clean_text = normalize_arabic(text)
                
                for key, pattern in patterns.items():
                    matches = pattern.findall(clean_text)
                    for match in matches:
                        entry = f"[{surah_num}:{ayah_num}] {match} (Orig: {text})"
                        results[key].append(entry)

        with open("d:\\KuranTaskent\\donkey_results.txt", "w", encoding="utf-8") as out:
            out.write(f"--- Sonuçlar ---\n")
            total_all = 0
            for key, items in results.items():
                out.write(f"\n{key}: {len(items)} adet\n")
                for item in items:
                    out.write(item + "\n")
                total_all += len(items)
                
            out.write(f"\nGENEL TOPLAM: {total_all}\n")
            print(f"Sonuçlar 'donkey_results.txt' dosyasına yazıldı.")

    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    main()
