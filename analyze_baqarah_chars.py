
import json
import unicodedata

def analyze_all_chars(text, description):
    counts = {}
    
    for char in text:
        cp = ord(char)
        hex_cp = f"{cp:04x}"
        if hex_cp not in counts:
            counts[hex_cp] = {'count': 0, 'char': char, 'name': unicodedata.name(char, 'UNKNOWN')}
        counts[hex_cp]['count'] += 1
            
    print(f"\n--- {description} ---")
    print(f"Total Length: {len(text)}")
    print("Character Counts:")
    
    # Sort by count descending
    sorted_chars = sorted(counts.items(), key=lambda x: x[1]['count'], reverse=True)
    
    for code, info in sorted_chars:
        # print name and count
        # Avoid printing the char itself if it causes encoding issues in some consoles, 
        # but here we'll try to be safe or just print code/name.
        print(f"  {code} : {info['count']} ({info['name']})")
        
    return counts

def main():
    try:
        with open('d:/KuranTaskent/quran_arabic.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Get Surah Baqarah (ID 2)
        baqarah = next((s for s in data if s['id'] == 2), None)
        
        # Get Fatiha (ID 1) to get Basmala text
        fatiha = next((s for s in data if s['id'] == 1), None)
        basmala = fatiha['verses'][0]['text']
        
        baqarah_text = ""
        for verse in baqarah['verses']:
            baqarah_text += verse['text']
            
        full_text = basmala + baqarah_text
        
        analyze_all_chars(full_text, "Full Text (Basmala + Baqarah)")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
