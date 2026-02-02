import json
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

def count_from_verse_16():
    try:
        with open('quran_arabic.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: quran_arabic.json not found.")
        return

    surah_neml = next((s for s in data if s['id'] == 27), None)
    
    # Range: Verse 16 to 20
    start_verse = 16
    end_verse = 20
    
    word_count = 0
    words_list = []
    
    print(f"--- NEML SURESİ 16-20 ARASI KELİME ANALİZİ ---")
    
    for verse in surah_neml['verses']:
        vid = verse['id']
        if vid < start_verse: continue
        if vid > end_verse: break
        
        text = verse['text']
        words = text.split()
        
        for w in words:
            # Normalize for checking target
            normalized = re.sub(r'[أإآٱ]', 'ا', w)
            normalized = re.sub(r'[\u064B-\u065F\u0670\u0617-\u061A\u06D6-\u06ED\u0640]', '', normalized)
            
            # Stop if we hit Hudhud in verse 20
            if vid == 20 and "هدهد" in normalized:
                word_count += 1
                words_list.append(w)
                print(f"HEDEF ULAŞILDI: {w} (Sıra: {word_count})")
                break
            
            word_count += 1
            words_list.append(w)

    print(f"\nToplam Kelime Sayısı (16. ayet başından Hüthüt'e kadar): {word_count}")
    
    # Check "Tayr" in verse 16 as start point?
    print(f"\n--- TAYR (16) -> HUDHUD (20) KONTROLÜ ---")
    
    tayr_index = -1
    for i, w in enumerate(words_list):
        normalized = re.sub(r'[أإآٱ]', 'ا', w)
        normalized = re.sub(r'[\u064B-\u065F\u0670\u0617-\u061A\u06D6-\u06ED\u0640]', '', normalized)
        if "طير" in normalized and tayr_index == -1:
            tayr_index = i
            print(f"Tayr (Kuş) bulundu: {w} (Index: {i+1})")
            
    if tayr_index != -1:
        count_between = word_count - tayr_index 
        # Inclusive count?
        print(f"Tayr'dan Hüthüt'e kadar olan mesafe (kelime sayısı): {count_between}")
    else:
        print("16. ayette 'Tayr' kelimesi listenin başında bulunamadı (belki ortalardadır).")

if __name__ == "__main__":
    count_from_verse_16()
