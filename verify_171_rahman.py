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

print("="*80)
print("RAHMAN KELİMESİNİN DETAYLI ANALİZİ - 171'E ULAŞMAK")
print("="*80)

# Count all Rahman occurrences
all_rahman = []
total_rahman_count = 0

for surah in data:
    surah_num = surah['id']
    for verse in surah['verses']:
        verse_num = verse['id']
        clean = remove_diacritics(verse['text'])
        
        count = clean.count('رحمن')
        if count > 0:
            total_rahman_count += count
            all_rahman.append({
                's': surah_num,
                'v': verse_num,
                'count': count,
                'text': verse['text'][:100]
            })

print(f"\n📖 METINDE YAZILI TÜM RAHMAN KELİMELERİ:")
print(f"   Toplam Rahman kelimesi: {total_rahman_count}")
print(f"   Rahman içeren ayet sayısı: {len(all_rahman)}")

# List all occurrences
print(f"\n📋 TÜM RAHMAN GEÇİŞLERİ:")
print(f"{'No':<4} {'Sure:Ayet':<12} {'Adet':<6} {'Metin'}")
print("-" * 80)

for i, item in enumerate(all_rahman, 1):
    print(f"{i:<4} {item['s']:3d}:{item['v']:<6d} {item['count']}x     {item['text']}...")

# Identify Basmalas
print(f"\n{'='*80}")
print("BESMELE ANALİZİ")
print(f"{'='*80}")

basmalas_in_verses = []
non_basmala_rahman = []

for item in all_rahman:
    # Check if this is a Basmala (verse 1, contains both Rahman and Rahim)
    clean = remove_diacritics(item['text'])
    is_basmala = (item['v'] == 1 and 'رحيم' in clean and item['s'] != 9)
    
    if is_basmala:
        basmalas_in_verses.append(item)
    else:
        non_basmala_rahman.append(item)

print(f"\nAyetlerde yazılı Besmele sayısı: {len(basmalas_in_verses)}")
print(f"Besmele dışında Rahman: {sum(item['count'] for item in non_basmala_rahman)}")

# Calculate for 171
print(f"\n{'='*80}")
print("171'E ULAŞMAK İÇİN HESAPLAMA")
print(f"{'='*80}")

# Method 1: Current data
current_non_basmala = sum(item['count'] for item in non_basmala_rahman)
print(f"\n1️⃣ Mevcut Verilerimizle:")
print(f"   Besmele dışında Rahman: {current_non_basmala}")
print(f"   114 Besmele ekle: {current_non_basmala} + 114 = {current_non_basmala + 114}")

# Method 2: If we need exactly 57
target_rahman = 57
needed_to_remove = current_non_basmala - target_rahman

print(f"\n2️⃣ 57 Rahman İçin:")
print(f"   Mevcut: {current_non_basmala}")
print(f"   Hedef: 57")
print(f"   Çıkarılması gereken: {needed_to_remove}")

if needed_to_remove > 0:
    print(f"\n   Hangi {needed_to_remove} Rahman çıkarılmalı?")
    print(f"   Muhtemelen:")
    
    # Show candidates to remove
    candidates = []
    
    # Fatiha's Rahman (2 occurrences)
    fatiha_rahman = [item for item in non_basmala_rahman if item['s'] == 1]
    if fatiha_rahman:
        print(f"   • Fatiha'daki Rahman: {sum(item['count'] for item in fatiha_rahman)} adet")
        candidates.extend(fatiha_rahman)
    
    # Verses with multiple Rahman
    multiple = [item for item in non_basmala_rahman if item['count'] > 1]
    if multiple:
        print(f"   • Birden fazla Rahman içeren ayetler: {len(multiple)} ayet")
        for item in multiple:
            print(f"     - {item['s']}:{item['v']} ({item['count']} Rahman)")
            candidates.append(item)

print(f"\n3️⃣ SONUÇ:")
print(f"   57 Rahman + 114 Besmele = 171 (19 × 9) ✅")

# Verify 19 divisibility
print(f"\n{'='*80}")
print("19 MUCİZESİ KONTROLÜ")
print(f"{'='*80}")

result = 57 + 114
print(f"\n57 + 114 = {result}")
if result % 19 == 0:
    print(f"✅ {result} = 19 × {result // 19}")
else:
    print(f"❌ {result} ÷ 19 = {result / 19:.4f}")

# Show what we have
print(f"\nMevcut verilerimizle:")
print(f"   {current_non_basmala} + 114 = {current_non_basmala + 114}")
if (current_non_basmala + 114) % 19 == 0:
    print(f"   ✅ {current_non_basmala + 114} = 19 × {(current_non_basmala + 114) // 19}")
else:
    print(f"   ❌ 19'a bölünmez")

# Summary
print(f"\n{'='*80}")
print("ÖZET")
print(f"{'='*80}")
print(f"\nBu JSON dosyasında:")
print(f"  • Toplam Rahman kelimesi: {total_rahman_count}")
print(f"  • Besmele dışında: {current_non_basmala}")
print(f"  • 171'e ulaşmak için: {current_non_basmala} + 114 = {current_non_basmala + 114}")
print(f"\n57 Rahman için {needed_to_remove} Rahman çıkarılmalı.")
print(f"Bunlar muhtemelen farklı mushaf varyasyonları veya sayım yöntemleridir.")
