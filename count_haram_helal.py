import json
import re
import sys

# Force UTF-8 output for Windows terminals
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def normalize_arabic(text):
    text = re.sub(r'[\u0670]', '\u0627', text) # Replace dagger alif with normal alif
    text = re.sub(r'[\u0623\u0625\u0622]', '\u0627', text) # Normalize Hamzas (أ, إ, آ) to bare Alif (ا)
    text = re.sub(r'[\u064B-\u065F]', '', text) # Remove harakat
    text = re.sub(r'[\u06D6-\u06ED]', '', text) # Remove waqf marks
    return text

def analyze_haram_helal():
    with open('quran_arabic.json', 'r', encoding='utf-8') as f:
        quran = json.load(f)
    
    # Kelime kökleri ve formları
    # Haram (H-R-M)
    # Halal (H-L-L)
    
    definitions = {
        "Haram (Noun/Adj - حرام)": {
            "patterns": [r"^حرام$"],
            "count": 0,
            "locations": []
        },
        "Halal (Noun/Adj - حلال)": {
            "patterns": [r"^حلال$"],
            "count": 0,
            "locations": []
        },
         "Harrama (Verb - حرم)": {
            "patterns": [r"حرم"],
            "count": 0,
            "locations": []
        },
        "Ahalla (Verb - احل)": {
            "patterns": [r"احل"],
            "count": 0,
            "locations": []
        }
    }

    results = {
        "haram_exact": [],
        "halal_exact": [],
        "harrama_verb": [],
        "ahalla_verb": []
    }

    print("Analyzing Quran for Haram and Helal...")

    for surah in quran:
        for ayah in surah['verses']:
            text = normalize_arabic(ayah['text'])
            words = text.split()
            
            for i, word in enumerate(words):
                # Clean word for comparison (remove prefixes like wa, fa, la if needed, but exact match is better first)
                clean_word = word
                
                # 1. Exact "Haram" (حرام)
                if "حرام" in clean_word:
                     # Filter out Mescid-i Haram occurrences
                     # Check previous word if possible, or check full ayah text
                     is_mescid_haram = False
                     if i > 0:
                         prev_word = normalize_arabic(words[i-1])
                         if "مسجد" in prev_word: # al-Masjid al-Haram
                             is_mescid_haram = True
                     
                     if not is_mescid_haram:
                         results["haram_exact"].append({
                             "s": surah['id'],
                             "a": ayah['id'],
                             "w": word
                         })
                     else:
                         # Optional: Track Mescid-i Haram separately if needed
                         pass

                # 2. Exact "Halal" (حلال)
                if "حلال" in clean_word:
                    results["halal_exact"].append({
                             "s": surah['id'],
                             "a": ayah['id'],
                             "w": word
                         })

                if "حرم" in clean_word:
                     results["harrama_verb"].append({
                         "s": surah['id'],
                         "a": ayah['id'],
                         "w": word
                     })

                # 4. Verb "Ahalla" (احل) -> Broaden to root H-L-L to see all
                # Root H-L-L matches: Halal, Ahalla, Tahilla, Yuhillu...
                if re.search(r'ح.*ل.*ل', clean_word):
                    results["ahalla_verb"].append({
                             "s": surah['id'],
                             "a": ayah['id'],
                             "w": word
                         })
                
    print(f"Total 'Haram' (containing حرام) found: {len(results['haram_exact'])}")
    print(f"Total 'Halal' (containing حلال) found: {len(results['halal_exact'])}")
    print(f"Total 'Haram' Root (containing حرم anywhere): {len(results['harrama_verb'])}")
    print(f"Total 'Halal' Root (containing ح..ل..ل): {len(results['ahalla_verb'])}")
    
    # Print distinct words found for Halal root to check validity
    halal_words = set([x['w'] for x in results['ahalla_verb']])
    print("\nDistinct Halal Root Words Found:")
    for w in sorted(halal_words):
        print(w)

    # Print distinct words found for Haram root to check validity
    haram_words = set([x['w'] for x in results['harrama_verb']])
    print("\nDistinct Haram Root Words Found:")
    for w in sorted(haram_words):
        print(w)

    print(f"Total 'Haram' (containing حرام, no Mescid): {len(results['haram_exact'])}")
    print(f"Total 'Halal' (containing حلال): {len(results['halal_exact'])}")
    
    print("\n--- Haram Occurrences (Context Analysis) ---")
    for item in results["haram_exact"]:
        print(f"[{item['s']}:{item['a']}] Word: {item['w']}") 
        # Ideally we would print the full verse here if we had access to the variable holding it
        # Since 'item' only has metadata, let's find the verse text from 'quran' object
        # This is slow O(N) lookup but fine for 11 items
        for s in quran:
            if s['id'] == item['s']:
                for a in s['verses']:
                    if a['id'] == item['a']:
                         print(f"Text: {a['text']}")
                         break
    
    print("\n--- Helal Occurrences (Context Analysis) ---")
    for item in results["halal_exact"]:
        print(f"[{item['s']}:{item['a']}] Word: {item['w']}")
        for s in quran:
            if s['id'] == item['s']:
                for a in s['verses']:
                    if a['id'] == item['a']:
                         print(f"Text: {a['text']}")
                         break

    # Save to file
    with open('haram_helal_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    analyze_haram_helal()
