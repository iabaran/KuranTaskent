# -*- coding: utf-8 -*-
import json
import sys
import re
sys.stdout.reconfigure(encoding='utf-8')

# Load data
with open('quran_arabic.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def remove_diacritics(text):
    arabic_diacritics = re.compile(r'[\u064B-\u065F\u0670\u0617-\u061A\u06D6-\u06ED]')
    return arabic_diacritics.sub('', text)

print("="*70)
print("114 BESMELE + 57 RAHMAN = 171 HESABI")
print("="*70)

# Count Rahman in verses (excluding Basmalas)
rahman_in_verses = 0
rahman_locations = []

for surah in data:
    surah_num = surah['id']
    for verse in surah['verses']:
        verse_num = verse['id']
        clean = remove_diacritics(verse['text'])
        
        # Count Rahman
        count = clean.count('رحمن')
        if count > 0:
            # Check if this is a Basmala (verse 1, contains both Rahman and Rahim)
            is_basmala = (verse_num == 1 and 'رحيم' in clean and surah_num != 9)
            
            if is_basmala:
                # This is a Basmala, don't count it in verses
                pass
            else:
                # This is a regular verse with Rahman
                rahman_in_verses += count
                for _ in range(count):
                    rahman_locations.append((surah_num, verse_num))

print(f"\n📖 BESMELE DIŞINDA RAHMAN:")
print(f"   Ayetlerdeki Rahman: {rahman_in_verses}")

# Count Basmalas
# All surahs except Tawbah (9) have Basmala = 113
# But we need to check if we should count 114
basmalas_113 = 113  # Traditional count (114 surahs - 1 Tawbah)
basmalas_114 = 114  # If we count something else

print(f"\n📿 BESMELE SAYISI:")
print(f"   Geleneksel (Tevbe hariç): 113")
print(f"   Kullanıcı önerisi: 114")

# Calculate totals
total_with_113 = rahman_in_verses + basmalas_113
total_with_114 = rahman_in_verses + basmalas_114

print(f"\n🔢 TOPLAM RAHMAN:")
print(f"   113 Besmele ile: {rahman_in_verses} + 113 = {total_with_113}")
print(f"   114 Besmele ile: {rahman_in_verses} + 114 = {total_with_114}")

# Check what we need for 171
target = 171
needed_basmalas = target - rahman_in_verses

print(f"\n🎯 171'E ULAŞMAK İÇİN:")
print(f"   Hedef: 171")
print(f"   Ayetlerdeki Rahman: {rahman_in_verses}")
print(f"   Gerekli Besmele: 171 - {rahman_in_verses} = {needed_basmalas}")

# Check for 57
print(f"\n🔍 57 RAHMAN NASIL BULUNUR?")

# Method 1: Only count specific Rahman (not in Basmalas)
rahman_non_basmala = 0
for surah in data:
    surah_num = surah['id']
    for verse in surah['verses']:
        verse_num = verse['id']
        clean = remove_diacritics(verse['text'])
        
        if 'رحمن' in clean:
            # Skip Basmalas (verse 1 with both Rahman and Rahim)
            is_basmala = (verse_num == 1 and 'رحيم' in clean and surah_num != 9)
            
            if not is_basmala:
                rahman_non_basmala += clean.count('رحمن')

print(f"   Besmele dışında Rahman: {rahman_non_basmala}")

# If we need 57, what should we exclude?
if rahman_non_basmala > 57:
    diff = rahman_non_basmala - 57
    print(f"   57'ye ulaşmak için {diff} Rahman çıkarılmalı")
    print(f"   {rahman_non_basmala} - {diff} = 57 ✅")

# Final calculation
print(f"\n{'='*70}")
print("SONUÇ")
print(f"{'='*70}")
print(f"\nEğer:")
print(f"  • Besmele dışında 57 Rahman sayarsak")
print(f"  • 114 Besmele eklersek")
print(f"  • TOPLAM = 57 + 114 = 171 (19 × 9) ✅")

print(f"\nŞu anki verilerimizde:")
print(f"  • Besmele dışında Rahman: {rahman_non_basmala}")
print(f"  • 57'ye ulaşmak için: {rahman_non_basmala} - {rahman_non_basmala - 57} = 57")
print(f"  • 114 Besmele ekle: 57 + 114 = 171")

# Check 19 divisibility
print(f"\n19 MUCİZESİ:")
if 171 % 19 == 0:
    print(f"✅ 171 = 19 × {171 // 19}")
else:
    print(f"❌ 171 ÷ 19 = {171 / 19:.2f} (tam bölünmüyor)")

# Also check what we have
print(f"\nMevcut sayılarımızla:")
print(f"  • {rahman_non_basmala} + 114 = {rahman_non_basmala + 114}")
print(f"  • {rahman_non_basmala} + 113 = {rahman_non_basmala + 113}")
