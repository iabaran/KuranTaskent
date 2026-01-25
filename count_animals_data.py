import json
import re

def normalize_arabic(text):
    text = re.sub(r'[\u064B-\u065F\u0670\u0610-\u061A\u06D6-\u06ED]', '', text)
    text = re.sub(r'[أإآٱ]', 'ا', text)
    return text

def main():
    file_path = "d:\\KuranTaskent\\quran_arabic.json"
    output_file = "d:\\KuranTaskent\\animals_data.js"
    
    # Desenler
    patterns = {
        "Himar": re.compile(r"\b(?:[وفلبك]?(?:ال)?)?حمار(?:ه|ها|هما|هم|كم|نا|ي|ك)?\b"), # Tekil
        "Hamir": re.compile(r"\b(?:[وفلبك]?(?:ال)?)?حمير(?:ه|ها|هما|هم|كم|نا|ي|ك)?\b"), # Çoğul
        "Humur": re.compile(r"\b(?:[وفلبك]?(?:ال)?)?حمر(?:ه|ها|هما|هم|كم|نا|ي|ك)?\b")  # Yaban (Humur) + Renk (35:27)
    }

    data = {
        "Esek": {"count": 0, "locations": [], "words": []}
    }

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            quran_data = json.load(f)

        for surah in quran_data:
            surah_num = surah["id"]
            for verse in surah["verses"]:
                ayah_num = verse["id"]
                text = verse["text"]
                clean_text = normalize_arabic(text)
                
                for key, pattern in patterns.items():
                    matches = pattern.findall(clean_text)
                    for match in matches:
                        # FİLTRELER
                        
                        # 35:27 "Humrun" (Kırmızı) -> Atla
                        if surah_num == 35 and ayah_num == 27:
                            continue
                            
                        # Veriye ekle
                        data["Esek"]["count"] += 1
                        data["Esek"]["locations"].append({
                            "s": surah_num,
                            "a": ayah_num,
                            "w": match
                        })
                        data["Esek"]["words"].append(match)

        # JSON to JS format
        js_content = "const animalsData = " + json.dumps(data, ensure_ascii=False, indent=4) + ";"
        
        with open(output_file, 'w', encoding='utf-8') as out:
            out.write(js_content)
            
        print(f"Animals data saved to {output_file}")
        print(f"Total Donkey Count: {data['Esek']['count']}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
