import json
import re
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def count_lafzullah_baqara():
    with open('quran_arabic.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    baqara = data[1]
    
    allah_word = "الله" # Without tashkeel usually.
    # In Uthmani script, it's often written with specific marks.
    # Let's use a regex to find Allah lafzı regardless of tashkeel.
    
    # \u0627\u0644\u0644\u0640?\u0647
    # But often there are shaddahs, hamzas etc.
    # Better to normalize and count.
    
    def normalize(text):
        noise = re.compile(r'[\u0610-\u061A\u064B-\u065F\u06D6-\u06ED\u08E4-\u08FE\u0670\u0671]')
        return re.sub(noise, '', text)

    count_allah = 0
    clean_allah = normalize("الله")
    
    for v in baqara['verses']:
        norm_v = normalize(v['text'])
        # We need to count whole words "الله"
        words = norm_v.split()
        for w in words:
            if w == clean_allah:
                count_allah += 1
                
    print(f"Lafzullah (Allah) count in Bakara: {count_allah}")
    print(f"Verses in Bakara: {len(baqara['verses'])}")

if __name__ == "__main__":
    count_lafzullah_baqara()
