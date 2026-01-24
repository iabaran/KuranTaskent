import json

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

data = load_json('d:/KuranTaskent/quran_arabic.json')
basmala = data[0]['verses'][0]['text']

# Character mappings
ALIF = ['\u0627', '\u0671']  # ا + ٱ
LAM = '\u0644'  # ل
MIM = '\u0645'  # م
RA = '\u0631'   # ر
SAD = '\u0635'  # ص
TA = '\u0637'   # ط
SIN = '\u0633'  # س
HA = '\u062d'   # ح
KAF = '\u0643'  # ك
HE = '\u0647'   # ه
YA = '\u064a'   # ي
AYN = '\u0639'  # ع
QAF = '\u0642'  # ق
NUN = '\u0646'  # ن

def get_surah_text(surah_id):
    surah = next(s for s in data if s['id'] == surah_id)
    return ''.join(v['text'] for v in surah['verses'])

def count_char(text, char):
    if isinstance(char, list):
        return sum(text.count(c) for c in char)
    return text.count(char)

def count_with_basmala(surah_id, chars):
    text = get_surah_text(surah_id)
    counts = {}
    for name, char in chars.items():
        surah_count = count_char(text, char)
        basmala_count = count_char(basmala, char)
        counts[name] = {
            'surah': surah_count,
            'basmala': basmala_count,
            'total': surah_count + basmala_count
        }
    return counts

# Define all Mukatta surahs and their letters
mukatta_surahs = [
    (2, 'Bakara', {'A': ALIF, 'L': LAM, 'M': MIM}),
    (3, 'Al-i Imran', {'A': ALIF, 'L': LAM, 'M': MIM}),
    (7, 'Araf', {'A': ALIF, 'L': LAM, 'M': MIM, 'S': SAD}),
    (10, 'Yunus', {'A': ALIF, 'L': LAM, 'R': RA}),
    (11, 'Hud', {'A': ALIF, 'L': LAM, 'R': RA}),
    (12, 'Yusuf', {'A': ALIF, 'L': LAM, 'R': RA}),
    (13, 'Rad', {'A': ALIF, 'L': LAM, 'M': MIM, 'R': RA}),
    (14, 'Ibrahim', {'A': ALIF, 'L': LAM, 'R': RA}),
    (15, 'Hicr', {'A': ALIF, 'L': LAM, 'R': RA}),
    (19, 'Meryem', {'K': KAF, 'H': HE, 'Y': YA, 'A': AYN, 'S': SAD}),
    (20, 'Taha', {'T': TA, 'H': HE}),
    (26, 'Suara', {'T': TA, 'S': SIN, 'M': MIM}),
    (27, 'Neml', {'T': TA, 'S': SIN}),
    (28, 'Kasas', {'T': TA, 'S': SIN, 'M': MIM}),
    (29, 'Ankebut', {'A': ALIF, 'L': LAM, 'M': MIM}),
    (30, 'Rum', {'A': ALIF, 'L': LAM, 'M': MIM}),
    (31, 'Lokman', {'A': ALIF, 'L': LAM, 'M': MIM}),
    (32, 'Secde', {'A': ALIF, 'L': LAM, 'M': MIM}),
    (36, 'Yasin', {'Y': YA, 'S': SIN}),
    (38, 'Sad', {'S': SAD}),
    (40, 'Mumin', {'H': HA, 'M': MIM}),
    (41, 'Fussilet', {'H': HA, 'M': MIM}),
    (42, 'Sura', {'H': HA, 'M': MIM, 'A2': AYN, 'S': SIN, 'Q': QAF}),
    (43, 'Zuhruf', {'H': HA, 'M': MIM}),
    (44, 'Duhan', {'H': HA, 'M': MIM}),
    (45, 'Casiye', {'H': HA, 'M': MIM}),
    (46, 'Ahkaf', {'H': HA, 'M': MIM}),
    (50, 'Kaf', {'Q': QAF}),
    (68, 'Kalem', {'N': NUN}),
]

print("=" * 80)
print("MUKATTA LETTER COUNTS (with Basmala)")
print("=" * 80)

for surah_id, name, chars in mukatta_surahs:
    counts = count_with_basmala(surah_id, chars)
    
    surah_freq_parts = []
    grand_total_parts = []
    total_sum = 0
    
    for letter, info in counts.items():
        surah_freq_parts.append(f"{letter}: {info['surah']}")
        grand_total_parts.append(f"{letter}: {info['total']}")
        total_sum += info['total']
    
    surah_freq = ", ".join(surah_freq_parts)
    grand_total = ", ".join(grand_total_parts)
    
    # Check if divisible by 19
    div_19 = ""
    if total_sum % 19 == 0:
        div_19 = f" = 19x{total_sum // 19}"
    
    print(f"Surah {surah_id} ({name}):")
    print(f"  surahFreq: {surah_freq}")
    print(f"  grandTotal: {grand_total} ({total_sum}{div_19})")
    print()
