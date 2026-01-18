# -*- coding: utf-8 -*-
import json
import sys
import re
sys.stdout.reconfigure(encoding='utf-8')

# Load data
with open('quran_arabic.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Function to remove all diacritics
def remove_diacritics(text):
    arabic_diacritics = re.compile(r'[\u064B-\u065F\u0670\u0617-\u061A\u06D6-\u06ED]')
    return arabic_diacritics.sub('', text)

# Collect Rahman and Rahim locations from verses
rahman_locations = []
rahim_locations = []

for surah in data:
    surah_num = surah['id']
    
    for verse in surah['verses']:
        verse_num = verse['id']
        text = verse['text']
        clean_text = remove_diacritics(text)
        
        # Count Rahman occurrences in this verse
        rahman_count = clean_text.count('رحمن')
        for _ in range(rahman_count):
            rahman_locations.append((surah_num, verse_num))
        
        # Count Rahim occurrences in this verse
        rahim_count = clean_text.count('رحيم')
        for _ in range(rahim_count):
            rahim_locations.append((surah_num, verse_num))

# Add Basmalas for surahs 2-8 and 10-114 (excluding 1 and 9)
# These are the "virtual" Basmalas not counted as separate verses
basmala_surahs = []
for i in range(2, 115):  # 2 to 114
    if i != 9:  # Skip Tawbah
        basmala_surahs.append(i)

# Generate JavaScript arrays
with open('rahman_rahim_data.js', 'w', encoding='utf-8') as f:
    # Rahman data
    f.write('// Rahman Data - 177 occurrences (65 verses + 112 Basmalas)\n')
    f.write('const rahmanData = [\n')
    
    # Add Basmalas first (surahs 2-8, 10-114)
    f.write('    // Basmalas (112 occurrences)\n')
    for i, s in enumerate(basmala_surahs):
        f.write(f'    {{ s: {s}, h: 1, w: "رحمن" }},\n')
    
    # Add verse occurrences
    f.write('    // Verse occurrences (65)\n')
    for i, (s, v) in enumerate(rahman_locations):
        comma = "," if i < len(rahman_locations) - 1 else ""
        f.write(f'    {{ s: {s}, a: {v}, w: "رحمن" }}{comma}\n')
    f.write('];\n\n')
    
    # Rahim data
    f.write('// Rahim Data - 227 occurrences (115 verses + 112 Basmalas)\n')
    f.write('const rahimData = [\n')
    
    # Add Basmalas first
    f.write('    // Basmalas (112 occurrences)\n')
    for i, s in enumerate(basmala_surahs):
        f.write(f'    {{ s: {s}, h: 1, w: "رحيم" }},\n')
    
    # Add verse occurrences
    f.write('    // Verse occurrences (115)\n')
    for i, (s, v) in enumerate(rahim_locations):
        comma = "," if i < len(rahim_locations) - 1 else ""
        f.write(f'    {{ s: {s}, a: {v}, w: "رحيم" }}{comma}\n')
    f.write('];\n')

print(f"✅ Dosya oluşturuldu: rahman_rahim_data.js")
print(f"   Rahman: {len(rahman_locations) + len(basmala_surahs)}")
print(f"   Rahim: {len(rahim_locations) + len(basmala_surahs)}")
