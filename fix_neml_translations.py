# -*- coding: utf-8 -*-
"""
Neml suresi 29, 30, 31. ayetlerin yanlış Türkçe meallerini düzelten script.
"""
import json
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# JSON dosyasını yükle
with open('quran_data/quran_tr.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=" * 80)
print("NEML SURESİ 29, 30, 31. AYETLERİN DÜZELTİLMESİ")
print("=" * 80)

# Eski değerleri göster
print("\n📋 ESKİ DEĞERLER (YANLIŞ):")
print("-" * 80)
print(f"29: {data['27']['ayahs']['29']}")
print(f"30: {data['27']['ayahs']['30']}")
print(f"31: {data['27']['ayahs']['31']}")

# Doğru mealleri ata
correct_translations = {
    "29": "(Melike) dedi ki: Ey ileri gelenler! Bana değerli bir mektup bırakıldı.",
    "30": "O (mektup) Süleyman'dandır ve şöyledir: Bismillahirrahmanirrahim (Rahman ve Rahim olan Allah'ın adıyla).",
    "31": "Bana karşı büyüklük taslamayın ve Müslüman olarak bana gelin."
}

# Güncelle
data['27']['ayahs']['29'] = correct_translations['29']
data['27']['ayahs']['30'] = correct_translations['30']
data['27']['ayahs']['31'] = correct_translations['31']

print("\n✅ YENİ DEĞERLER (DOĞRU):")
print("-" * 80)
print(f"29: {data['27']['ayahs']['29']}")
print(f"30: {data['27']['ayahs']['30']}")
print(f"31: {data['27']['ayahs']['31']}")

# Kaydet
with open('quran_data/quran_tr.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("\n" + "=" * 80)
print("✅ BAŞARIYLA DÜZELTİLDİ!")
print("=" * 80)
print("\nAçıklama:")
print("  • 29. Ayet: Melike'nin mektup geldiğini söylemesi")
print("  • 30. Ayet: Mektubun Süleyman'dan olduğu ve Besmele ile başladığı")
print("  • 31. Ayet: Mektubun içeriği (teslim olun emri)")
print("\n💡 Not: 30. ayette 'Bismillahirrahmanirrahim' geçer - bu yüzden")
print("   Neml 27:30'da 'Rahim' kelimesi bulunur!")
