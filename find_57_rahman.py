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
print("57 RAHMAN'I BULMAK İÇİN FARKLI VARYASYONLAR")
print("="*70)

# Try different variations
variations = {
    'الرحمن (Al-Rahman)': 'الرحمن',
    'رحمن (Rahman without Al)': 'رحمن',
    'ٱلرَّحۡمَٰنِ (with specific diacritics)': 'ٱلرَّحۡمَٰنِ',
    'ٱلرَّحۡمَٰن (without final kasra)': 'ٱلرَّحۡمَٰن',
}

for name, pattern in variations.items():
    count = 0
    locations = []
    for surah in data:
        for verse in surah['verses']:
            occurrences = verse['text'].count(pattern)
            if occurrences > 0:
                count += occurrences
                for _ in range(occurrences):
                    locations.append((surah['id'], verse['id']))
    
    print(f"\n{name}: {count}")
    if count > 0 and count <= 10:
        print(f"  Konumlar: {locations}")

# Try normalized version (no diacritics)
print(f"\n{'='*70}")
print("NORMALİZE EDİLMİŞ ARAMA (Hareke olmadan)")
print(f"{'='*70}")

rahman_normalized = 0
rahman_with_al = 0
rahman_without_al = 0

for surah in data:
    for verse in surah['verses']:
        clean = remove_diacritics(verse['text'])
        
        # Count الرحمن (with Al)
        count_with_al = clean.count('الرحمن')
        rahman_with_al += count_with_al
        
        # Count standalone رحمن (without Al, not preceded by ال)
        # This is tricky, we need to check context
        text = clean
        pos = 0
        while True:
            pos = text.find('رحمن', pos)
            if pos == -1:
                break
            # Check if preceded by ال
            if pos >= 2 and text[pos-2:pos] == 'ال':
                # This is الرحمن, already counted
                pass
            else:
                # This is standalone رحمن
                rahman_without_al += 1
            pos += 1

rahman_normalized = rahman_with_al + rahman_without_al

print(f"الرحمن (Al-Rahman): {rahman_with_al}")
print(f"رحمن (standalone): {rahman_without_al}")
print(f"Toplam: {rahman_normalized}")

# Special case: Count only specific forms
print(f"\n{'='*70}")
print("ÖZEL DURUM: SADECE BELİRLİ FORMLARI SAYMA")
print(f"{'='*70}")

# Maybe they only count Rahman when it appears as a name (not in Basmala context)
rahman_non_basmala = 0
locations_non_basmala = []

for surah in data:
    surah_num = surah['id']
    for verse in surah['verses']:
        verse_num = verse['id']
        clean = remove_diacritics(verse['text'])
        
        # Skip if this looks like a Basmala (contains both Rahman and Rahim)
        if 'رحمن' in clean:
            # Check if it's in a Basmala context
            is_basmala = ('رحيم' in clean and verse_num == 1 and surah_num != 9)
            
            if not is_basmala:
                count = clean.count('رحمن')
                rahman_non_basmala += count
                for _ in range(count):
                    locations_non_basmala.append((surah_num, verse_num))

print(f"Rahman (Besmele dışında): {rahman_non_basmala}")
print(f"İlk 10 konum: {locations_non_basmala[:10]}")

# Check if 57 can be achieved
print(f"\n{'='*70}")
print("57'YE ULAŞMAK İÇİN")
print(f"{'='*70}")

print(f"\nMetindeki Rahman: 65")
print(f"65 - 8 = 57 (19 × 3) ✅")
print(f"\nYani 8 Rahman'ı çıkarmamız gerekiyor.")
print(f"Muhtemelen:")
print(f"  • Fatiha'daki 2 Rahman (1:1 ve 1:3)")
print(f"  • Bazı tekrarlanan veya özel durumlar")
print(f"\nAlternatif: Sadece 'الرحمن' (Al-Rahman) formunu saymak")

# Count only الرحمن with Al prefix
only_al_rahman = 0
for surah in data:
    for verse in surah['verses']:
        clean = remove_diacritics(verse['text'])
        only_al_rahman += clean.count('الرحمن')

print(f"\nSadece 'الرحمن' (Al- ile): {only_al_rahman}")
if only_al_rahman == 57:
    print("✅ BULUNDU! 57 = 19 × 3")
