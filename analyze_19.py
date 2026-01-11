import json
import re
import sys

# Windows terminal fix for Arabic characters
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def normalize_arabic(text):
    if not text: return ""
    # Remove all diacritics and signs
    # Includes Tashkeel, small high signs, pause marks, dagger alif, etc.
    noise = re.compile(r'[\u0610-\u061A\u064B-\u065F\u06D6-\u06ED\u08E4-\u08FE\u0670]')
    text = re.sub(noise, '', text)
    
    # Normalize Alef variants to plain Alef (\u0627)
    # Includes Alef Wasla (\u0671), Alef with Madda (\u0622), Alef with Hamza (\u0623, \u0625)
    alef_variants = re.compile(r'[\u0622\u0623\u0625\u0671]')
    text = re.sub(alef_variants, '\u0627', text)
    
    # Normalize other chars
    text = re.sub(r'[\u0624\u0626]', '\u0621', text) # Hamza variants
    
    return text

# Ebced (Abjad) Numerical Values Mapping
EBCED_TABLE = {
    '\u0627': 1,    # Alif
    '\u0628': 2,    # Ba
    '\u062c': 3,    # Jim
    '\u062f': 4,    # Dal
    '\u0647': 5,    # He
    '\u0648': 6,    # Waw
    '\u0632': 7,    # Ze
    '\u062d': 8,    # Haa
    '\u0637': 9,    # Taa (Soft)
    '\u064a': 10,   # Ya
    '\u0643': 20,   # Kaf
    '\u0644': 30,   # Lam
    '\u0645': 40,   # Mim
    '\u0646': 50,   # Nun
    '\u0633': 60,   # Sin
    '\u0639': 70,   # Ain
    '\u0641': 80,   # Fe
    '\u0635': 90,   # Sad
    '\u0642': 100,  # Qaf
    '\u0631': 200,  # Ra
    '\u0634': 300,  # Shin
    '\u062a': 400,  # Ta (Hard)
    '\u062b': 500,  # Tha
    '\u062e': 600,  # Kha
    '\u0630': 700,  # Thal
    '\u0636': 800,  # Dad
    '\u0638': 900,  # Za
    '\u063a': 1000  # Ghain
}

def calculate_ebced(text):
    norm_text = normalize_arabic(text)
    total = 0
    for char in norm_text:
        if char in EBCED_TABLE:
            total += EBCED_TABLE[char]
    return total

def analyze():
    try:
        with open('quran_arabic.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading file: {e}")
        return

    print("=== QURAN 19 MIRACLE ANALYSIS ===\n")

    # 1. Basmala Letter Count
    # Standard claim: Basmala consists of 19 letters
    # (B-S-M A-L-L-H A-L-R-H-M-N A-L-R-H-Y-M)
    b_raw = data[0]['verses'][0]['text'] # Surah 1:1
    b_norm = normalize_arabic(b_raw).replace(" ", "")
    print(f"--- Basmala Letter Count ---")
    print(f"Original: {b_raw}")
    print(f"Normalized: {b_norm}")
    print(f"Letter Count: {len(b_norm)} (Is 19? {len(b_norm) == 19})")

    # 2. General Stats
    total_surahs = len(data)
    print(f"\n--- General Statistics ---")
    print(f"Total Surahs: {total_surahs} (114? {total_surahs == 114})")
    
    total_verses = sum(len(s['verses']) for s in data)
    print(f"Total Verses: {total_verses} (6236? {total_verses == 6236}, 6236 = 19 * {total_verses / 19:.2f})")

    # 3. Word counts (Basmalah words)
    # The 19 miracle claims often count the unnumbered Basmalas at the start of 112 surahs
    # (Surahs 2-8 and 10-114). Surah 1:1 is counted as a verse, and Surah 9 has no Basmala.
    
    basmala_text = normalize_arabic("بسم الله الرحمن الرحيم")
    basmala_count = 112 # Unnumbered ones
    
    raw_text = ""
    for surah in data:
        for idx, verse in enumerate(surah['verses']):
            v_text = normalize_arabic(verse['text'])
            # Eğer 1. ayet ise ve içinde Besmele geçiyorsa (Fatiha hariç)
            # API bazen 1. ayetin başına Besmele'yi yapıştırıyor.
            if idx == 0 and surah['id'] != 1 and basmala_text in v_text:
                v_text = v_text.replace(basmala_text, "").strip()
            raw_text += " " + v_text

    def count_word(text, word, include_basmalas=True):
        count = text.count(word)
        if include_basmalas:
            count += basmala_text.count(word) * basmala_count
        return count

    targets = [
        {"name": "Ism", "word": normalize_arabic("اسم"), "claim": 19},
        {"name": "Allah", "word": normalize_arabic("الله"), "claim": 2698},
        {"name": "Rahman", "word": normalize_arabic("رحمن"), "claim": 57},
        {"name": "Rahim", "word": normalize_arabic("رحيم"), "claim": 114}
    ]

    print("\n--- Word Occurrences (including unnumbered Basmalas) ---")
    print(f"{'Name':<10} | {'Count':<10} | {'Claim':<10} | {'Status':<15}")
    print("-" * 50)
    for t in targets:
        count = count_word(raw_text, t['word'])
        status = "MATCH!" if count == t['claim'] else f"Diff: {count - t['claim']}"
        divisible = count % 19 == 0
        div_str = f" (19*{count//19})" if divisible else ""
        print(f"{t['name']:<10} | {count:<10} | {t['claim']:<10} | {status}{div_str}")

    # 4. Huruf-u Mukattaa Analysis (Example: Qaf)
    # Surah 42 and 50 contain 'Qaf'
    print("\n--- Qaf Analysis (Surahs 42 and 50) ---")
    qaf = normalize_arabic("ق")
    q_count_42 = 0
    q_count_50 = 0
    
    for surah in data:
        if surah['id'] == 42:
            for v in surah['verses']:
                q_count_42 += normalize_arabic(v['text']).count(qaf)
        if surah['id'] == 50:
            for v in surah['verses']:
                q_count_50 += normalize_arabic(v['text']).count(qaf)
                
    total_q = q_count_42 + q_count_50
    print(f"Q count in S42: {q_count_42}")
    print(f"Q count in S50: {q_count_50}")
    print(f"Total Q: {total_q} (57 + 57 = 114? {total_q == 114}, 114 = 19 * 6)")
    
    # 5. Ebced (Abjad) Analysis
    print("\n--- Ebced (Abjad) Values ---")
    ebced_targets = [
        {"name": "Allah", "text": "الله"},
        {"name": "Basmala", "text": "بسم الله الرحمن الرحيم"},
        {"name": "Muhammad", "text": "محمد"},
        {"name": "Islam", "text": "اسلام"}
    ]
    for e in ebced_targets:
        val = calculate_ebced(e['text'])
        print(f"{e['name']} ({e['text']}): {val}")

if __name__ == "__main__":
    analyze()
