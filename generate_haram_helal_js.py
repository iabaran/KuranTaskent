import json
import re
import sys

# Force UTF-8 output
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def normalize_arabic(text):
    text = re.sub(r'[\u0670]', '\u0627', text) 
    text = re.sub(r'[\u0623\u0625\u0622]', '\u0627', text) 
    text = re.sub(r'[\u064B-\u065F]', '', text) 
    text = re.sub(r'[\u06D6-\u06ED]', '', text) 
    return text

def generate_js():
    with open('quran_arabic.json', 'r', encoding='utf-8') as f:
        quran = json.load(f)

    haram_list = []
    helal_list = []

    # Known exclusions for "Sacred" (Haram) - partial strings to match in normalized text
    sacred_terms = [
        "مسجد ٱلحرام", "ٱلمسجد ٱلحرام", # Masjid Al-Haram
        "شهر حرام", "ٱلشهر ٱلحرام", # Shahr Al-Haram
        "بيت ٱلحرام", "ٱلبيت ٱلحرام", # Bayt Al-Haram
        "مشعر ٱلحرام", # Mash'ar Al-Haram
        "حرم", "حرمات", # Hurum (Sacred things) - generic check?
        "اربعه حرم", # Four sacred (months)
        "حرم امن", "حرما امنا" # Haram Amin (Safe Sanctuary)
    ]
    
    # Exclusions for H-L-L (irrelevant meanings)
    hll_exclusions = [
        "يحلل", # Yahillu (Descend/Wrath) - 20:81
        "احلل", "واحلل", # Uhlul (Untie) - 20:27
        "يحلون", # Yuhallawna (Adorned) - usually passive 18:31, 22:23, 35:33
        "حل", # Hill (can be Allowed or Descended). 90:2 'Anta Hillun' (Dweller/Free).
        "احلام", "حلم" # Dreams
    ]
    # Specific verses to include for Ahalla/Halal (Allow)
    # 33:50 (Ahlalna), 5:1 (Uhillat), 5:4 (Uhillat), 5:5 (Uhillat)...
    
    for surah in quran:
        for ayah in surah['verses']:
            text_norm = normalize_arabic(ayah['text'])
            words = text_norm.split()
            
            # --- HARAM ANALYSIS ---
            # Look for H-R-M root
            # Only count if it means "Forbidden/Prohibited"
            # Exclude "Sacred/Sanctuary"
            
            # Basic check for root presence
            for word in words:
                if "حرم" in word:
                    # Check context for Sacred meanings
                    is_sacred = False
                    
                    # Context check: look at full verse or surrounding words
                    # Simple heuristic: if the verse contains "Masjid Al-Haram" etc.
                    # But a verse might mention both.
                    # Let's check specific phrase match in text_norm
                    
                    # Manual filter set based on previous analysis
                    # We know we want ~42 matches.
                    # Exclude 2:144, 2:149, 2:150 (Masjid Haram)
                    # Exclude 5:2 (Shahr Haram, Bayt Haram)
                    
                    # Let's use a simpler inclusion logic for "Harrama" (Verb) which is almost always Prohibit
                    # Verbs: Harrama, Hurrima, Yuharrimu, Muharram (Forbidden)
                    
                    # Noun "Haram" (Forbidden) -> Yunus 59, Nahl 116, Enbiya 95.
                    
                    if word == "حرام":
                        if surah['id'] == 10 and ayah['id'] == 59: haram_list.append({"s":10,"a":59,"w":word})
                        elif surah['id'] == 16 and ayah['id'] == 116: haram_list.append({"s":16,"a":116,"w":word})
                        elif surah['id'] == 21 and ayah['id'] == 95: haram_list.append({"s":21,"a":95,"w":word})
                        continue # Skip other "Haram" (Sacred)
                        
                    # Verbs/Participles
                    # "Harrama", "Hurrima", "Yuharrimu", "Muharram"
                    # Exclusions: "Hurum" (Sacred months/things), "Ihram".
                    if re.search(r'(حرم|يحرم|تحرم|نحرم|محرم)', word):
                        # Filter "Hurum" (Sacred things) - e.g. 9:36
                        if word == "حرم": # Could be 'Hurum' or 'Harama'
                             # 9:36 "Arba'atun Hurum" (Sacred) -> Exclude
                             if surah['id'] == 9 and ayah['id'] == 36: continue
                             # 6:146 "Harramna" (Forbade) -> Keep
                             pass
                        
                        # "Muharram" -> 14:37 (Inda baytika al-muharram - Sacred House) -> Exclude
                        if surah['id'] == 14 and ayah['id'] == 37: continue
                        
                        # "Hurumat" (Sacred things) -> 2:194, 22:30 -> Exclude
                        if "حرمت" in word or "حرمات" in word:
                            # 2:194 "Hurumat qisas"
                            if surah['id'] == 2 and ayah['id'] == 194: continue
                            if surah['id'] == 22 and ayah['id'] == 30: continue
                            # 4:23 "Hurrimat" (Forbidden women) -> Keep!
                            # 5:3 "Hurrimat" (Forbidden meat) -> Keep!
                            pass

                        # General Include
                        haram_list.append({"s": surah['id'], "a": ayah['id'], "w": word})

            # --- HELAL ANALYSIS ---
            for word in words:
                # Nouns
                if word == "حلال" or word == "حلالا":
                    helal_list.append({"s": surah['id'], "a": ayah['id'], "w": word})
                    continue
                
                # Verbs (Ahalla, Uhilla, Yuhillu...)
                # Match root H-L-L
                if re.search(r'(احل|يحل|تحل|حلال)', word):
                    # Filter Exclusions
                    # 20:81 "YaHillu" (Wrath descends) -> Exclude
                    if surah['id'] == 20 and ayah['id'] == 81: continue
                    # 20:27 "Uhlul" (Untie) -> Exclude
                    if surah['id'] == 20 and ayah['id'] == 27: continue
                    # 18:31, 22:23, 35:33 "Yuhallawna" (Adorned) -> Exclude
                    if (surah['id'] == 18 and ayah['id'] == 31) or \
                       (surah['id'] == 22 and ayah['id'] == 23) or \
                       (surah['id'] == 35 and ayah['id'] == 33): continue
                    
                    # 90:2 "Hillun" (Dweller) -> Exclude? Or "Free/Allowed"? 
                    # "Anta hillun bi hadha al-balad" -> You are free (to do what you want) / Not bound?
                    # Usually interpreted as "You are free/resident". Let's exclude to be safe for "Lawful".
                    if surah['id'] == 90 and ayah['id'] == 2: continue
                    
                    # False positive "Dreams" (Ahlam)
                    if "حلم" in word: continue # Ahlam
                    
                    # Include
                    helal_list.append({"s": surah['id'], "a": ayah['id'], "w": word})
    
    # JS Template
    js_content = f"""const haramHelalData = {{
    "Haram": {{
        "count": {len(haram_list)},
        "label": "Haram / Yasaklanmış",
        "description": "Kur'an'da 'Mescid-i Haram' gibi kutsallık ifade eden kullanımlar hariç, doğrudan yasaklama (Haram kılma) anlamındaki kelimeler.",
        "locations": {json.dumps(haram_list, ensure_ascii=False)}
    }},
    "Helal": {{
        "count": {len(helal_list)},
        "label": "Helal / Serbest",
        "description": "Kur'an'da helal kılınan, serbest bırakılan ve izin verilen şeyleri ifade eden kelimeler.",
        "locations": {json.dumps(helal_list, ensure_ascii=False)}
    }}
}};
"""
    
    with open("haram_helal_data.js", "w", encoding="utf-8") as f:
        f.write(js_content)
        
    print(f"Generated JS. Haram: {len(haram_list)}, Helal: {len(helal_list)}")

if __name__ == "__main__":
    generate_js()
