# -*- coding: utf-8 -*-
import json
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Arapça metni yükle
with open('quran_arabic.json', 'r', encoding='utf-8') as f:
    arabic_data = json.load(f)

# Türkçe meali yükle
with open('quran_data/quran_tr.json', 'r', encoding='utf-8') as f:
    turkish_data = json.load(f)

# Neml suresini bul
neml_ar = [s for s in arabic_data if s['id'] == 27][0]
neml_tr = turkish_data['27']  # Türkçe JSON'da sure numarası string key

print("=" * 80)
print("NEML SURESİ 29, 30, 31. AYETLERİN KARŞILAŞTIRMASI")
print("=" * 80)

for verse_num in [29, 30, 31]:
    print(f"\n{'='*80}")
    print(f"AYET 27:{verse_num}")
    print(f"{'='*80}")
    
    # Arapça
    arabic_verse = neml_ar['verses'][verse_num - 1]
    print(f"\nArapça:")
    print(f"  {arabic_verse['text']}")
    
    # Türkçe
    turkish_verse = neml_tr['ayahs'][str(verse_num)]
    print(f"\nTürkçe Meal:")
    print(f"  {turkish_verse}")

print("\n" + "=" * 80)
print("SONUÇ:")
print("=" * 80)

# Mealleri karşılaştır
meal_29 = neml_tr['ayahs']['29']
meal_30 = neml_tr['ayahs']['30']
meal_31 = neml_tr['ayahs']['31']

if meal_29 == meal_30 == meal_31:
    print("❌ UYARI: 29, 30 ve 31. ayetlerin Türkçe mealleri TAMAMEN AYNI!")
    print(f"\nOrtak meal: {meal_29}")
else:
    print("✓ Mealler farklı.")
    if meal_29 == meal_30:
        print("  - 29 ve 30. ayetler aynı")
    if meal_30 == meal_31:
        print("  - 30 ve 31. ayetler aynı")
    if meal_29 == meal_31:
        print("  - 29 ve 31. ayetler aynı")
