import json

# Load Quran JSON (Arabic text)
with open(r'd:/KuranTaskent/quran_arabic.json', encoding='utf-8') as f:
    data = json.load(f)

# Basmala is first verse of Surah 1 (Fatiha)
basmala = data[0]['verses'][0]['text']
# Surah Baqarah (id 2)
baqarah = next(s for s in data if s['id'] == 2)
baqarah_text = ''.join(v['text'] for v in baqarah['verses'])
full = basmala + baqarah_text

# Plain Alif (U+0627)
alif_plain = full.count('ا')
# All Alif variants (including Wasla, Hamza, Madda, Superscript, Maqsura)
alif_variants = ['ا','ٱ','أ','إ','آ','ٰ','ى']
alif_all = sum(full.count(ch) for ch in alif_variants)

lam = full.count('ل')
mim = full.count('م')

print('Plain Alif (ا)      :', alif_plain)
print('All Alif variants   :', alif_all)
print('Lam (ل)            :', lam)
print('Mim (م)            :', mim)
print('Total (plain)      :', alif_plain + lam + mim)
print('Total (all variants):', alif_all   + lam + mim)
