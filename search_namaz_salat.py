import json
import re

# Kuran verilerini yükle
with open('quran_arabic.json', 'r', encoding='utf-8') as f:
    quran_data = json.load(f)

print("=" * 80)
print("NAMAZ (SALAT) İLE İLGİLİ AYETLER")
print("=" * 80)
print()

# Namaz ile ilgili anahtar kelimeler (Arapça kökler)
# صلاة (salat) - namaz
# صلى (salla) - namaz kılmak
# يصلي (yusalli) - namaz kılıyor
# صلوا (sallu) - namaz kılın

salat_patterns = [
    'صلاة',   # salat (namaz)
    'صلوة',   # salat (alternatif yazım)
    'الصلاة', # es-salat (namaz)
    'الصلوة', # es-salat (alternatif)
    'صلى',    # salla (namaz kıldı)
    'يصل',    # yusalli (namaz kılıyor)
    'صلوا',   # sallu (namaz kılın)
    'تصل',    # tusalli (namaz kılıyorsun)
    'نصل',    # nusalli (namaz kılıyoruz)
]

results = []

# Her sure ve ayeti tara
for surah in quran_data['data']['surahs']:
    surah_number = surah['number']
    surah_name = surah['name']
    surah_name_tr = surah.get('englishName', '')
    
    for ayah in surah['ayahs']:
        ayah_number = ayah['number']
        ayah_text = ayah['text']
        ayah_number_in_surah = ayah['numberInSurah']
        
        # Namaz kelimesini ara
        for pattern in salat_patterns:
            if pattern in ayah_text:
                results.append({
                    'surah_number': surah_number,
                    'surah_name': surah_name,
                    'surah_name_tr': surah_name_tr,
                    'ayah_number': ayah_number_in_surah,
                    'ayah_text': ayah_text,
                    'matched_pattern': pattern
                })
                break  # Bir ayet için bir kez ekle

# Sonuçları göster
print(f"Toplam {len(results)} ayet bulundu\n")
print("=" * 80)

for i, result in enumerate(results, 1):
    print(f"\n{i}. {result['surah_name']} ({result['surah_name_tr']}) - Ayet {result['ayah_number']}")
    print(f"   Sure: {result['surah_number']}, Ayet: {result['ayah_number']}")
    print(f"   Arapça: {result['ayah_text']}")
    print("-" * 80)

print(f"\n\nTOPLAM: {len(results)} ayet")

# İstatistikler
print("\n" + "=" * 80)
print("İSTATİSTİKLER")
print("=" * 80)

# Sure bazında sayım
surah_counts = {}
for result in results:
    surah_name = f"{result['surah_name']} ({result['surah_name_tr']})"
    surah_counts[surah_name] = surah_counts.get(surah_name, 0) + 1

print("\nSure bazında namaz ayetleri:")
for surah_name, count in sorted(surah_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"  {surah_name}: {count} ayet")
