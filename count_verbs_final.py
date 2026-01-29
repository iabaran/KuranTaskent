import json
import re
import sys

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def normalize_arabic(text):
    text = re.sub(r'[\u0670]', '\u0627', text) 
    text = re.sub(r'[\u0623\u0625\u0622]', '\u0627', text) 
    text = re.sub(r'[\u064B-\u065F]', '', text) 
    text = re.sub(r'[\u06D6-\u06ED]', '', text) 
    return text

def analyze():
    with open('quran_arabic.json', 'r', encoding='utf-8') as f:
        quran = json.load(f)

    # 1. FORBIDDEN (H-R-M)
    # Includes: Haram (noun), Harrama (verb), Hurrima (passive), Yuharrimu, Muharram
    # Exclude: I don't need to exclude much, H-R-M is mostly relevant. 
    # Just need to manually check "Sacred" (Hurum, Ihram) vs "Forbidden".
    
    haram_matches = []
    
    # 2. ALLOWED (H-L-L)
    # Includes: Halal (noun), Ahalla (verb), Uhilla (passive), Yahillu (be lawful)
    # Exclude: H-M-L (Carry), H-L-F (Swear), H-L-Q (Shave), H-L-Y (Adorn), H-L-M (Dream)
    
    halal_matches = []
    
    for surah in quran:
        for ayah in surah['verses']:
            text = normalize_arabic(ayah['text'])
            words = text.split()
            
            for word in words:
                # HARAM CHECK
                if "حرم" in word:
                    # Capture all H-R-M for manual review 
                    # (Filtering Mescid-i Haram is easy later)
                    haram_matches.append({
                        "loc": f"{surah['id']}:{ayah['id']}", 
                        "w": word,
                        "text": text
                    })

                # HALAL CHECK
                # Must contain H and L and L? Or just H and L (Ahalla = A-H-L)
                # Ahalla (احل) -> A - H - L. Shadda lost.
                # So we search for word containing "احل" OR "يحل" OR "حلال"
                
                # Exclude if it has M (Haml), F (Half), Q (Halq), Y (Haly - except Yahillu ends with Y/I logic? No, Yahillu ends with L)
                # Yahillu -> يحل.
                # Haly -> حلي.
                
                # Precise targets for 'Allowed' verbs/nouns:
                if (
                    "احل" in word or # Ahalla, Uhilla, Ahlalna...
                    "يحل" in word or # Yahillu
                    "تحل" in word or # Tahillu
                    "حلال" in word   # Halal
                ):
                    # Filter out False Positives
                    if "حمل" in word or "حلم" in word or "حلف" in word or "حلق" in word:
                        continue 
                    # Adornment (Haly) check: "يحلون" (Yuhallawna - they are adorned) vs "يحلون" (Yahilluna - they allow/legitimize)
                    # Textual context needed? normalize removes harakat so "YuHalla" and "YaHillu" look same "يحل".
                    # 18:31, 22:23, 35:33 -> Yuhallawna (Adorned).
                    
                    halal_matches.append({
                        "loc": f"{surah['id']}:{ayah['id']}", 
                        "w": word,
                        "text": text
                    })

    print(f"Total H-R-M matches found: {len(haram_matches)}")
    print(f"Total H-L-L (Allowed-like) matches found: {len(halal_matches)}")

    print("\n--- POSSIBLE 'ALLOWED' (HELAL) MATCHES ---")
    for m in halal_matches:
        print(f"[{m['loc']}] {m['w']}")

    print("\n--- POSSIBLE 'FORBIDDEN' (HARAM) MATCHES ---")
    # Just print the first few non-standard ones or all to simple count
    for m in haram_matches:
         print(f"[{m['loc']}] {m['w']}")

if __name__ == "__main__":
    analyze()
