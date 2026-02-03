import json
import re

file_path = r'd:\KuranTaskent\quran_tr_js.js'

def search_quran():
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract JSON part
        # content format is like: const GLOBAL_QURAN_TR = { ... }
        match = re.search(r'const GLOBAL_QURAN_TR = ({.*})', content, re.DOTALL)
        if not match:
            print("Could not find JSON object in file.")
            if len(content) > 100:
                 print(f"Content start: {content[:100]}...")
            return

        json_str = match.group(1)
        # Parse JSON
        try:
            quran_data = json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            # Try to fix potential trailing commas or other JS specific syntax if simple load fails
            # For now, assume it's valid JSON
            return

        keywords = ["şarap", "içki", "sarhoş"]
        found_verses = []

        print(f"Searching for keywords: {keywords}")
        print("-" * 50)

        for surah_num, surah_data in quran_data.items():
            surah_name = surah_data.get('name', '')
            surah_name_en = surah_data.get('englishName', '')
            ayahs = surah_data.get('ayahs', {})

            for ayah_num, ayah_text in ayahs.items():
                lower_text = ayah_text.lower()
                for kw in keywords:
                    if kw in lower_text:
                        found_verses.append({
                            'surah_num': surah_num,
                            'surah_name': surah_name,
                            'surah_name_en': surah_name_en,
                            'ayah_num': ayah_num,
                            'text': ayah_text,
                            'keyword': kw
                        })
                        break # Avoid duplicates if multiple keywords in one verse

        if not found_verses:
            print("No verses found with these keywords.")
        else:
            print(f"Found {len(found_verses)} verses:\n")
            for v in found_verses:
                print(f"Surah {v['surah_num']} ({v['surah_name_en']}) Verse {v['ayah_num']}:")
                # Highlight keyword
                text = v['text']
                # specific highlight not strictly necessary for output, just printing text
                print(f"{text}\n")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    search_quran()
