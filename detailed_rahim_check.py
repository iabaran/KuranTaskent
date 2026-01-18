# -*- coding: utf-8 -*-
import json
import re
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def normalize_arabic(text):
    """Arapça metni normalize et (harekeleri kaldır)"""
    if not text:
        return ""
    # Hareke ve diğer işaretleri kaldır
    text = re.sub(r'[\u064B-\u065F\u0670]', '', text)
    return text.strip()

# Load JSON
with open('quran_arabic.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=" * 80)
print("RAHİM KELİMESİNİN DETAYLI KONTROLÜ")
print("=" * 80)

# Rahim kelimesini ara
rahim_pattern = 'رحيم'
total_count = 0
besmele_in_verse_1 = 0
other_verses = []

for surah in data:
    surah_id = surah['id']
    surah_name = surah['transliteration']
    
    for verse in surah['verses']:
        verse_id = verse['id']
        text = verse['text']
        normalized = normalize_arabic(text)
        
        count = normalized.count(rahim_pattern)
        if count > 0:
            total_count += count
            
            if verse_id == 1:
                besmele_in_verse_1 += count
                print(f"\n✓ Sure {surah_id:3d} ({surah_name}), Ayet 1 - {count} Rahim")
                print(f"  {text}")
            else:
                other_verses.append({
                    'surah': surah_id,
                    'surah_name': surah_name,
                    'verse': verse_id,
                    'text': text,
                    'count': count
                })

print("\n" + "=" * 80)
print("DİĞER AYETLER (İlk ayet olmayan):")
print("=" * 80)

for item in other_verses[:20]:  # İlk 20 örnek
    print(f"\nSure {item['surah']:3d} ({item['surah_name']}), Ayet {item['verse']:3d} - {item['count']} Rahim")
    print(f"  {item['text']}")

if len(other_verses) > 20:
    print(f"\n... ve {len(other_verses) - 20} adet daha")

print("\n" + "=" * 80)
print("ÖZET:")
print("=" * 80)
print(f"İlk ayetlerdeki Rahim (besmele): {besmele_in_verse_1}")
print(f"Diğer ayetlerdeki Rahim: {sum(item['count'] for item in other_verses)}")
print(f"TOPLAM: {total_count}")
print("=" * 80)

# Özel kontrol: Neml 30
print("\n" + "=" * 80)
print("ÖZEL KONTROL: NEML SURESİ 30. AYET")
print("=" * 80)
neml = [s for s in data if s['id'] == 27][0]
verse_30 = neml['verses'][29]  # Index 29 = Ayet 30
print(f"Metin: {verse_30['text']}")
normalized = normalize_arabic(verse_30['text'])
print(f"Normalize: {normalized}")
print(f"'رحيم' var mı? {rahim_pattern in normalized}")
print(f"Kaç tane? {normalized.count(rahim_pattern)}")
