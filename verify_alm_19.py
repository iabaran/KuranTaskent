import json

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

data = load_json('d:/KuranTaskent/quran_arabic.json')

# Surahs starting with A.L.M, A.L.M.S, A.L.M.R, A.L.R
alm_surahs = [2, 3, 7, 10, 11, 12, 13, 14, 15, 29, 30, 31, 32]

# Characters to count
# 19-theory: Alif = ا (0627) and ٱ (0671)
alif_chars = ['\u0627', '\u0671']
lam_char = '\u0644'
mim_char = '\u0645'

# Basmala from Surah 1
basmala = data[0]['verses'][0]['text']

def count_alm(text):
    alif = sum(text.count(c) for c in alif_chars)
    lam = text.count(lam_char)
    mim = text.count(mim_char)
    return alif, lam, mim

grand_alif = 0
grand_lam = 0
grand_mim = 0

print(f"{'Surah':<15} | {'Alif':<6} | {'Lam':<6} | {'Mim':<6} | {'Total':<6}")
print("-" * 50)

for s_id in alm_surahs:
    surah = next(s for s in data if s['id'] == s_id)
    text = ''.join(v['text'] for v in surah['verses'])
    
    # Each of these Surahs has a Basmala header
    # (Surah 1's Basmala is numbered, but for Surah 2, 3, etc. it's the same text)
    s_alif, s_lam, s_mim = count_alm(text)
    b_alif, b_lam, b_mim = count_alm(basmala)
    
    # Total for this Surah including Basmala
    t_alif = s_alif + b_alif
    t_lam = s_lam + b_lam
    t_mim = s_mim + b_mim
    t_sum = t_alif + t_lam + t_mim
    
    grand_alif += t_alif
    grand_lam += t_lam
    grand_mim += t_mim
    
    print(f"Surah {s_id:<8} | {t_alif:<6} | {t_lam:<6} | {t_mim:<6} | {t_sum:<6}")

total_sum = grand_alif + grand_lam + grand_mim
print("-" * 50)
print(f"{'GRAND TOTAL':<15} | {grand_alif:<6} | {grand_lam:<6} | {grand_mim:<6} | {total_sum:<6}")
print(f"Grand Total / 19 = {total_sum / 19:.2f}")

if total_sum % 19 == 0:
    print("SUCCESS: Grand total is a multiple of 19!")
else:
    # Check if there's a 1-count discrepancy often mentioned in 19-theory
    print(f"DISCREPANCY: Remainder is {total_sum % 19}")
