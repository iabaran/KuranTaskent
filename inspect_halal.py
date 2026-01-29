import json
import re
import sys

# Force UTF-8 output
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def normalize_arabic(text):
    text = re.sub(r'[\u064B-\u065F\u0670]', '', text) # Remove harakat and superscripts
    text = re.sub(r'[\u06D6-\u06ED]', '', text) # Remove waqf marks
    return text

def inspect_verse():
    with open('quran_arabic.json', 'r', encoding='utf-8') as f:
        quran = json.load(f)
    
    # 2:168 (Surah 2, Ayah 168)
    surah = next((s for s in quran if s['id'] == 2), None)
    if surah:
        ayah = next((a for a in surah['verses'] if a['id'] == 168), None)
        if ayah:
            text = ayah['text']
            print(f"Original Text (2:168): {text}")
            
            normalized = normalize_arabic(text)
            print(f"Normalized Text: {normalized}")
            
            words = text.split()
            print("Words analysis:")
            for w in words:
                norm_w = normalize_arabic(w)
                print(f"Original: {w} -> Normalized: {norm_w}")
                if "حل" in norm_w:
                    print(f"^^^ Potential match? 'حل' found.")

if __name__ == "__main__":
    inspect_verse()
