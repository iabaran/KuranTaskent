import json
import re

def analyze_rahim_translation():
    try:
        # Load Arabic text (assuming it's available or known)
        # For now, I'll use a known list or just scan the Turkish file for 'merhamet' and 'bağışlayan'
        with open('d:/KuranTaskent/quran_tr_js.js', 'r', encoding='utf-8') as f:
            content = f.read()
            # Extract the JSON part
            match = re.search(r'const GLOBAL_QURAN_TR = (\{.*\});', content, re.DOTALL)
            if not match:
                print("Could not find JSON in Turkish file")
                return
            tr_data = json.loads(match.group(1))

        # We know Ar-Rahim (الرحيم) is 114 times in verses.
        # Let's see how often 'Bağışlayan' and 'Merhamet eden' appear.
        
        counts = {
            "Bağışlayan": 0,
            "Merhamet eden": 0,
            "Rahim": 0,
            "Esirgeyen": 0
        }
        
        for surah_id, surah in tr_data.items():
            for ay_id, text in surah['ayahs'].items():
                if "Bağışlayan" in text: counts["Bağışlayan"] += 1
                if "Merhamet eden" in text: counts["Merhamet eden"] += 1
                if "Rahim" in text: counts["Rahim"] += 1
                if "Esirgeyen" in text: counts["Esirgeyen"] += 1
        
        print(f"Turkish word counts in verses:")
        for word, count in counts.items():
            print(f"{word}: {count}")

    except Exception as e:
        print(f"Error: {e}")

analyze_rahim_translation()
