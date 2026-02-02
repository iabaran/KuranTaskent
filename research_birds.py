import json
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

def remove_diacritics(text):
    text = re.sub(r'[أإآٱ]', 'ا', text)
    text = re.sub(r'[\u064B-\u065F\u0670\u0617-\u061A\u06D6-\u06ED]', '', text)
    text = re.sub(r'\u0640', '', text)
    return text

def research_birds():
    try:
        with open('quran_arabic.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: quran_arabic.json not found.")
        return

    # Hudhud (Hoopoe) - الهدهد (usually al-hudhud)
    hudhud_term = "هدهد" 
    
    # Generic Bird terms (Tayr) - طير
    tayr_term = "طير"

    print("--- HÜTHÜT (HUDHUD) ARAŞTIRMASI ---")
    for surah in data:
        for verse in surah['verses']:
            text = verse['text']
            clean_text = remove_diacritics(text)
            
            if hudhud_term in clean_text:
                print(f"Hüthüt Bulundu: Sure {surah['id']} (Neml Suresi olabilir mi?), Ayet {verse['id']}")
                print(f"Arapça (Temiz): {clean_text}")
    
    print("\n--- GENEL KUŞ (TAYR) ARAŞTIRMASI ---")
    count_tayr = 0
    for surah in data:
        for verse in surah['verses']:
            clean_text = remove_diacritics(verse['text'])
            if tayr_term in clean_text:
                count_tayr += 1
                # print(f"Kuş Geçiyor: {surah['id']}:{verse['id']}")
    print(f"Toplam 'Tayr/Kuş' kökü geçen ayet sayısı: {count_tayr}")

if __name__ == "__main__":
    research_birds()
