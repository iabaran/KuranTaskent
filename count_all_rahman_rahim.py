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

# Count Rahman and Rahim
rahman_in_verses = []
rahim_in_verses = []

for surah in data:
    surah_num = surah['id']
    
    for verse in surah['verses']:
        verse_num = verse['id']
        text = verse['text']
        clean_text = remove_diacritics(text)
        
        # Count Rahman occurrences in this verse
        rahman_count = clean_text.count('رحمن')
        for _ in range(rahman_count):
            rahman_in_verses.append((surah_num, verse_num))
        
        # Count Rahim occurrences in this verse
        rahim_count = clean_text.count('رحيم')
        for _ in range(rahim_count):
            rahim_in_verses.append((surah_num, verse_num))

# Add Basmalas (113 surahs - excluding Surah 9 Tawbah)
# Each Basmala has 1 Rahman and 1 Rahim
basmala_count = 113  # Total surahs (114) - Tawbah (1)

total_rahman = len(rahman_in_verses) + basmala_count
total_rahim = len(rahim_in_verses) + basmala_count

print(f"{'='*70}")
print(f"📖 KUR'AN-I KERİM'DE RAHMAN VE RAHİM KELİMELERİ")
print(f"{'='*70}")

print(f"\n🔵 RAHMAN KELİMESİ:")
print(f"   Ayetlerde geçen:        {len(rahman_in_verses):3d}")
print(f"   Besmelelerde:          +{basmala_count:3d} (113 sure)")
print(f"   ─────────────────────────────")
print(f"   TOPLAM RAHMAN:          {total_rahman:3d}")

print(f"\n🔴 RAHİM KELİMESİ:")
print(f"   Ayetlerde geçen:        {len(rahim_in_verses):3d}")
print(f"   Besmelelerde:          +{basmala_count:3d} (113 sure)")
print(f"   ─────────────────────────────")
print(f"   TOPLAM RAHİM:           {total_rahim:3d}")

print(f"\n{'='*70}")
print(f"📊 ÖZET:")
print(f"   Rahman: {total_rahman} | Rahim: {total_rahim}")
print(f"{'='*70}")

# Save Rahman locations to file
print(f"\n💾 Rahman konumları kaydediliyor...")
with open('all_rahman_locations.txt', 'w', encoding='utf-8') as f:
    f.write(f"TÜM RAHMAN GEÇİŞLERİ ({total_rahman} adet)\n")
    f.write("="*60 + "\n\n")
    
    f.write("BESMELELERDEKİ RAHMAN (113 adet):\n")
    f.write("-"*60 + "\n")
    for i in range(1, 115):
        if i != 9:  # Skip Tawbah
            f.write(f"{i}:1 (Besmele)\n")
    
    f.write(f"\nAYETLERDEKİ RAHMAN ({len(rahman_in_verses)} adet):\n")
    f.write("-"*60 + "\n")
    for s, v in rahman_in_verses:
        f.write(f"{s}:{v}\n")

# Save Rahim locations to file
print(f"💾 Rahim konumları kaydediliyor...")
with open('all_rahim_locations.txt', 'w', encoding='utf-8') as f:
    f.write(f"TÜM RAHİM GEÇİŞLERİ ({total_rahim} adet)\n")
    f.write("="*60 + "\n\n")
    
    f.write("BESMELELERDEKİ RAHİM (113 adet):\n")
    f.write("-"*60 + "\n")
    for i in range(1, 115):
        if i != 9:  # Skip Tawbah
            f.write(f"{i}:1 (Besmele)\n")
    
    f.write(f"\nAYETLERDEKİ RAHİM ({len(rahim_in_verses)} adet):\n")
    f.write("-"*60 + "\n")
    for s, v in rahim_in_verses:
        f.write(f"{s}:{v}\n")

print(f"\n✅ Dosyalar kaydedildi:")
print(f"   - all_rahman_locations.txt ({total_rahman} Rahman)")
print(f"   - all_rahim_locations.txt ({total_rahim} Rahim)")
