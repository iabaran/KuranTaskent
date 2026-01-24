import re
import json

QURAN_FILE = "d:\\KuranTaskent\\quran_arabic.json"

def normalize_arabic(text):
    # Harekeler
    text = re.sub(r'[\u064B-\u065F\u0670]', '', text)
    # Alef varyasyonlarını normalleştir (أ, إ, آ, ٱ -> ا)
    text = re.sub(r'[أإآٱ]', 'ا', text)
    return text

def create_regex(core_pattern):
    prefix = r"(?:[وفلبك]?(?:ال)?)"
    suffix = r"(?:ون|ين|ات|ان|ة)?" 
    return re.compile(r"\b" + prefix + core_pattern + suffix + r"\b")

pattern = create_regex(r"منافق")

# Test Ayeti: Bakara 62 (Nasara geçiyor)
test_surah = 2
test_ayah = 62

pattern = create_regex(r"نصارى")

with open("debug_output.txt", "w", encoding="utf-8") as out:
    try:
        with open(QURAN_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        for s in data:
            if s["id"] == test_surah:
                for v in s["verses"]:
                    if v["id"] == test_ayah:
                        orig = v["text"]
                        clean = normalize_arabic(orig)
                        out.write(f"Original: {orig}\n")
                        out.write(f"Clean:    {clean}\n")
                        
                        matches = pattern.findall(clean)
                        out.write(f"Matches:  {matches}\n")
                        
                        # Manual regex check
                        manual_pattern = r"منافق"
                        if manual_pattern in clean:
                            out.write(f"Manual check '{manual_pattern}' FOUND in text!\n")
                        else:
                            out.write(f"Manual check '{manual_pattern}' NOT FOUND in text!\n")
                            
                        # Hex dump
                        hex_dump = " ".join("{:04x}".format(ord(c)) for c in clean)
                        out.write(f"Hex dump: {hex_dump}\n")
                        
                        break
                break
                
    except Exception as e:
        out.write(str(e))
