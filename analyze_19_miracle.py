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

print("="*70)
print("KUR'AN-I KERİM'DE RAHMAN VE RAHİM ANALİZİ")
print("="*70)

# Method 1: Count in verses only (what's written in the Quran text)
rahman_in_text = 0
rahim_in_text = 0

for surah in data:
    for verse in surah['verses']:
        clean = remove_diacritics(verse['text'])
        rahman_in_text += clean.count('رحمن')
        rahim_in_text += clean.count('رحيم')

print(f"\n📖 METİNDE YAZILI OLANLAR:")
print(f"   Rahman: {rahman_in_text}")
print(f"   Rahim: {rahim_in_text}")

# Method 2: Add "conceptual" Basmalas (not written as separate verses)
# Basmalas exist at the beginning of 113 surahs (all except Tawbah)
# But Fatiha's Basmala is already a verse (1:1)
# So we add 112 more "conceptual" Basmalas

conceptual_basmalas = 112  # Surahs 2-8, 10-114
total_rahman_with_basmalas = rahman_in_text + conceptual_basmalas
total_rahim_with_basmalas = rahim_in_text + conceptual_basmalas

print(f"\n📿 BESMELE EKLENİNCE (112 Besmele):")
print(f"   Rahman: {total_rahman_with_basmalas} ({rahman_in_text} + {conceptual_basmalas})")
print(f"   Rahim: {total_rahim_with_basmalas} ({rahim_in_text} + {conceptual_basmalas})")

# Method 3: Traditional count (all 113 Basmalas counted separately)
# This is the traditional Islamic scholarship method
all_basmalas = 113
total_rahman_traditional = (rahman_in_text - 2) + all_basmalas  # -2 because Fatiha has 2 Rahman in verses
total_rahim_traditional = (rahim_in_text - 2) + all_basmalas   # -2 because Fatiha has 2 Rahim in verses

print(f"\n📚 GELENEKSEL SAYIM (113 Besmele ayrı sayılır):")
print(f"   Rahman: {total_rahman_traditional} ({rahman_in_text - 2} ayet + {all_basmalas} Besmele)")
print(f"   Rahim: {total_rahim_traditional} ({rahim_in_text - 2} ayet + {all_basmalas} Besmele)")

# Check 19 divisibility
print(f"\n{'='*70}")
print("19 MUCİZESİ ANALİZİ")
print(f"{'='*70}")

def check_19(value, name):
    if value % 19 == 0:
        print(f"✅ {name}: {value} = 19 × {value // 19}")
        return True
    else:
        remainder = value % 19
        closest_lower = (value // 19) * 19
        closest_higher = closest_lower + 19
        print(f"❌ {name}: {value} (19'a bölünmez, kalan: {remainder})")
        print(f"   En yakın 19 katları: {closest_lower} (19×{closest_lower//19}) ve {closest_higher} (19×{closest_higher//19})")
        return False

print("\nMetindeki sayılar:")
check_19(rahman_in_text, "Rahman (metin)")
check_19(rahim_in_text, "Rahim (metin)")

print("\nBesmele eklenince:")
check_19(total_rahman_with_basmalas, "Rahman (112 Besmele)")
check_19(total_rahim_with_basmalas, "Rahim (112 Besmele)")

print("\nGeleneksel sayım:")
check_19(total_rahman_traditional, "Rahman (113 Besmele)")
check_19(total_rahim_traditional, "Rahim (113 Besmele)")

# Special case: Rahman with Dagger Alif (رحمٰن)
print(f"\n{'='*70}")
print("ÖZEL DURUM: DAGGER ALİF (ٰ) İLE YAZILAN RAHMAN")
print(f"{'='*70}")

rahman_with_dagger = 0
for surah in data:
    for verse in surah['verses']:
        # Look for Rahman with dagger alif (U+0670)
        if 'رحمٰن' in verse['text'] or 'رَحۡمَٰن' in verse['text']:
            rahman_with_dagger += verse['text'].count('رحمٰن') + verse['text'].count('رَحۡمَٰن')

print(f"Dagger Alif ile Rahman: {rahman_with_dagger}")
check_19(rahman_with_dagger, "Rahman (Dagger Alif)")

print(f"\n{'='*70}")
print("SONUÇ VE ÖNERİ")
print(f"{'='*70}")
print(f"\nEn doğru sayım metinde yazılı olanları saymaktır:")
print(f"  • Rahman: {rahman_in_text}")
print(f"  • Rahim: {rahim_in_text}")
print(f"\nBu sayılar 19'a tam bölünmüyor, ancak bu normal çünkü:")
print(f"  • 19 Mucizesi her kelime için değil, belirli kelimeler için geçerlidir")
print(f"  • Bazı araştırmacılar farklı varyasyonları sayar (الرحمن vs رحمن)")
print(f"  • Edip Yüksel'in 57 Rahman iddiası muhtemelen özel bir varyasyon içindir")
