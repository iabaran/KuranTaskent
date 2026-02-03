import json
import re

file_path = r'd:\KuranTaskent\quran_tr_js.js'

def check_verses():
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        match = re.search(r'const GLOBAL_QURAN_TR = ({.*})', content, re.DOTALL)
        if not match:
            print("JSON not found")
            return

        json_str = match.group(1)
        quran_data = json.loads(json_str)

        verses_to_check = [
            ('5', '90'),
            ('16', '67')
        ]

        for surah, ayah in verses_to_check:
            try:
                text = quran_data[surah]['ayahs'][ayah]
                print(f"Surah {surah} Verse {ayah}: {text}")
            except KeyError:
                print(f"Could not find Surah {surah} Verse {ayah}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_verses()
