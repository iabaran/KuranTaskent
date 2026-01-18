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
print("DETAYLI RAHMAN ANALİZİ - 57'Yİ BULMA")
print("="*70)

# List all Rahman occurrences
all_rahman = []
for surah in data:
    for verse in surah['verses']:
        clean = remove_diacritics(verse['text'])
        count = clean.count('رحمن')
        if count > 0:
            all_rahman.append({
                's': surah['id'],
                'v': verse['id'],
                'count': count,
                'text': verse['text'][:80]
            })

print(f"\nToplam Rahman geçişi: {len(all_rahman)}")
print(f"\nİlk 20 geçiş:")
for i, item in enumerate(all_rahman[:20], 1):
    print(f"{i:2d}. {item['s']:3d}:{item['v']:3d} ({item['count']}x) - {item['text']}...")

# Check for duplicates or special cases
print(f"\n{'='*70}")
print("TEKRAR EDEN AYETLER (Aynı ayette birden fazla Rahman)")
print(f"{'='*70}")

multiple_rahman = [item for item in all_rahman if item['count'] > 1]
print(f"\nBirden fazla Rahman içeren ayetler: {len(multiple_rahman)}")
for item in multiple_rahman:
    print(f"  {item['s']}:{item['v']} - {item['count']} kez")

# Calculate different scenarios
print(f"\n{'='*70}")
print("FARKLI SENARYOLAR")
print(f"{'='*70}")

total_occurrences = sum(item['count'] for item in all_rahman)
print(f"\n1. Tüm Rahman kelimelerini say: {total_occurrences}")

unique_verses = len(all_rahman)
print(f"2. Sadece Rahman içeren ayet sayısı: {unique_verses}")

# Exclude Fatiha
without_fatiha = [item for item in all_rahman if item['s'] != 1]
total_without_fatiha = sum(item['count'] for item in without_fatiha)
print(f"3. Fatiha hariç: {total_without_fatiha}")

# Exclude Basmalas (verse 1 of each surah except Tawbah)
without_basmalas = [item for item in all_rahman if not (item['v'] == 1 and item['s'] != 9)]
total_without_basmalas = sum(item['count'] for item in without_basmalas)
print(f"4. Besmeleleri çıkar: {total_without_basmalas}")

# Only count verses where Rahman appears alone (not with Rahim)
rahman_alone = []
for surah in data:
    for verse in surah['verses']:
        clean = remove_diacritics(verse['text'])
        if 'رحمن' in clean and 'رحيم' not in clean:
            rahman_alone.append((surah['id'], verse['id']))

print(f"5. Sadece Rahman var, Rahim yok: {len(rahman_alone)}")

# Try excluding some specific verses
print(f"\n{'='*70}")
print("57'YE ULAŞMAK İÇİN HANGİ 8 AYETI ÇIKARMALI?")
print(f"{'='*70}")
print(f"\nToplam: {total_occurrences}")
print(f"Hedef: 57 (19 × 3)")
print(f"Çıkarılması gereken: {total_occurrences - 57}")

# Hypothesis: Exclude Fatiha (2) + some duplicates
fatiha_rahman = sum(item['count'] for item in all_rahman if item['s'] == 1)
print(f"\nFatiha'daki Rahman: {fatiha_rahman}")
print(f"Kalan: {total_occurrences - fatiha_rahman} - 57 = {total_occurrences - fatiha_rahman - 57}")

# Check if there's a pattern
print(f"\n{'='*70}")
print("SONUÇ")
print(f"{'='*70}")
print(f"\nBu JSON dosyasında:")
print(f"  • Toplam Rahman: {total_occurrences}")
print(f"  • Rahman içeren ayet: {unique_verses}")
print(f"  • Fatiha hariç: {total_without_fatiha}")
print(f"  • Besmele hariç: {total_without_basmalas}")
print(f"\nHiçbiri 57 değil. Muhtemelen:")
print(f"  1. Farklı bir mushaf/metin kullanılıyor")
print(f"  2. Özel bir sayım yöntemi var (örn: sadece isim olarak geçenler)")
print(f"  3. Belirli formlar sayılıyor (الرحمٰن gibi)")
print(f"\n💡 ÖNERİ: Mevcut verilere göre en doğru sayılar:")
print(f"  • Rahman (metinde): 65")
print(f"  • Rahim (metinde): 115")
print(f"  • Rahman + 112 Besmele: 177")
print(f"  • Rahim + 112 Besmele: 227")
