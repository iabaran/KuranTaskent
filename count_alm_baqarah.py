import json, sys

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

data = load_json('d:/KuranTaskent/quran_arabic.json')
# Basmala is first verse of Surah 1 (Fatiha)
basmala = data[0]['verses'][0]['text']
# Baqarah is surah with id 2 (index 1)
baqarah = next(s for s in data if s['id'] == 2)
baqarah_text = ''.join(v['text'] for v in baqarah['verses'])
full = basmala + baqarah_text

print('Alif count:', full.count('ا'))
print('Lam count:', full.count('ل'))
print('Mim count:', full.count('م'))
