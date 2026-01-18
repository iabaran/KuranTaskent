import json

# Load Reference Data (The one with 88 counts)
with open('angel_satan_data.js', 'r', encoding='utf-8') as f:
    content = f.read()
    # Extract JSON part manually as it is JS file
    # const satanData = [...];
    satan_json = content.split('const satanData = ')[1].split(';')[0]
    angel_json = content.split('const angelData = ')[1].split(';')[0]
    
    ref_satan = json.loads(satan_json)
    ref_angel = json.loads(angel_json)

# Load New Data
with open('satan_data_with_words.js', 'r', encoding='utf-8') as f:
    content = f.read()
    new_satan = json.loads(content.split('= ')[1].split(';')[0])

with open('angel_data_with_words.js', 'r', encoding='utf-8') as f:
    content = f.read()
    new_angel = json.loads(content.split('= ')[1].split(';')[0])

print(f"Ref Satan: {len(ref_satan)} | New Satan: {len(new_satan)}")
print(f"Ref Angel: {len(ref_angel)} | New Angel: {len(new_angel)}")

# Find Missing Satan Verses
ref_satan_set = set((x['s'], x['a']) for x in ref_satan)
new_satan_set = set((x['s'], x['a']) for x in new_satan)
missing_satan = ref_satan_set - new_satan_set

print(f"Missing Satan Locations: {len(missing_satan)}")
sorted_missing = sorted(list(missing_satan))
print(f"Sample Missing Satan: {sorted_missing[:5]}")

# Find Missing Angel Verses
ref_angel_set = set((x['s'], x['a']) for x in ref_angel)
new_angel_set = set((x['s'], x['a']) for x in new_angel)
missing_angel = ref_angel_set - new_angel_set

print(f"Missing Angel Locations: {len(missing_angel)}")
sorted_missing_angel = sorted(list(missing_angel))
print(f"Sample Missing Angel: {sorted_missing_angel[:5]}")

# Load Quran to print text of missing
with open('quran_arabic.json', 'r', encoding='utf-8') as f:
    quran = json.load(f)

def get_text(s, a):
    surah = next(x for x in quran if x['id'] == s)
    verse = next(v for v in surah['verses'] if v['id'] == a)
    return verse['text']

print("\n--- Examining Missing Angels ---")
for s, a in sorted_missing_angel[:5]:
    txt = get_text(s, a)
    print(f"{s}:{a} -> {txt}")
