import json
import sys

# UTF-8 encoding için
sys.stdout.reconfigure(encoding='utf-8')

# Kuran verilerini yükle
with open('quran_arabic.json', 'r', encoding='utf-8') as f:
    quran_data = json.load(f)

print("=" * 80)
print("NAMAZ (SALAT) İLE İLGİLİ TÜM AYETLER")
print("=" * 80)
print()
print("NOT: Kuran'da namazın kaç rekat olduğuna dair DOĞRUDAN bir bilgi yoktur.")
print("Rekat sayıları Hz. Muhammed'in (s.a.v.) uygulamasından (sünnet) gelir.")
print()

results = []

# Her sure ve ayeti tara - "صل" kökünü içeren tüm kelimeleri bul
for surah in quran_data:
    surah_number = surah['id']
    surah_name = surah['name']
    surah_name_tr = surah.get('transliteration', '')
    
    for ayah in surah['verses']:
        ayah_number = ayah['id']
        ayah_text = ayah['text']
        
        # "صل" kökünü içeren kelimeleri ara (namaz ile ilgili)
        if 'صل' in ayah_text or 'صَل' in ayah_text or 'صَّل' in ayah_text:
            results.append({
                'surah_number': surah_number,
                'surah_name': surah_name,
                'surah_name_tr': surah_name_tr,
                'ayah_number': ayah_number,
                'ayah_text': ayah_text,
            })

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

# Önemli bilgi
print("\n" + "=" * 80)
print("ÖNEMLİ BİLGİ:")
print("=" * 80)
print("""
Kuran'da namazın:
- FARZ olduğu açıkça belirtilmiştir
- Vakitleri (sabah, öğle, ikindi, akşam, yatsı) işaret edilmiştir
- Nasıl kılınacağı (rükû, secde) anlatılmıştır
- Ancak KAÇ REKAT olduğu DOĞRUDAN belirtilmemiştir

Rekat sayıları:
- Hz. Muhammed'in (s.a.v.) uygulamasından (sünnet) gelir
- Hadislerde detaylı olarak anlatılmıştır
- İslam alimleri arasında icma (ittifak) vardır:
  * Sabah: 2 rekat farz
  * Öğle: 4 rekat farz
  * İkindi: 4 rekat farz
  * Akşam: 3 rekat farz
  * Yatsı: 4 rekat farz
""")
