#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Kur'an'da İsa (عيسى) ve Musa (موسى) kelimelerini sayan script
"""

import json
import re

# Quran Arabic JSON dosyasını yükle
with open('quran_arabic.json', 'r', encoding='utf-8') as f:
    quran = json.load(f)

# Harekesiz normalize etme fonksiyonu
def normalize_arabic(text):
    """Harekeler ve uzatma işaretlerini kaldır"""
    # Harekeler: fatha, damma, kasra, sukun, shadda, tanwin vb.
    # Ayrıca U+0670 (SUPERSCRIPT ALEF) gibi karakterleri de kaldırıyoruz
    diacritics = re.compile(r'[\u064B-\u065F\u0670\u06D6-\u06ED\u0640\u0653-\u0655]')
    return diacritics.sub('', text)

# Hedef kelimeler (Harekesiz)
targets = {
    'isa': {
        'pattern': 'عيسى',
        'display': 'İsa (عيسى)',
        'results': [],
        'count': 0
    },
    'musa': {
        'pattern': 'موسى',
        'display': 'Musa (موسى)',
        'results': [],
        'count': 0
    }
}

print("=" * 80)
print("İSA VE MUSA KELİMELERİ ANALİZİ")
print("=" * 80)

for surah in quran:
    surah_num = surah['id']
    surah_name = surah.get('name', f'Sure {surah_num}')
    
    for verse in surah['verses']:
        verse_num = verse['id']
        text = verse['text']
        normalized_text = normalize_arabic(text)
        
        # Kelimeleri ara
        for key, data in targets.items():
            pattern = data['pattern']
            
            # Tam kelime eşleşmesi için regex (kelimenin başında/sonunda harf olmamalı veya boşluk olmalı)
            # Ancak basitçe substring counts da yapabiliriz, çünkü bu isimler genelde kök olarak başka kelime içinde geçmez.
            # Yine de "el-Musa" gibi bağlamlar olabilir (gerçi özel isim).
            # En güvenlisi basit count, çünkü "bi-Musa", "wa-Musa" gibi bitişik yazımlar olabilir.
            
            # Basit string count (bu isimlerin başka kelimenin parçası olma ihtimali çok düşüktür)
            c = normalized_text.count(pattern)
            
            if c > 0:
                data['count'] += c
                data['results'].append({
                    's': surah_num,
                    'a': verse_num
                })

# Sonuçları yazdır
for key, data in targets.items():
    print(f"\n{data['display']}: {data['count']} kez")
    print(f"Örnek ayetler: {len(data['results'])} adet")

print("-" * 80)

# JavaScript dosyası oluştur
print("\nJS Dosyası çıktısı:")
js_content = ""
for key, data in targets.items():
    js_content += f"const {key}Data = [\n"
    for r in data['results']:
        js_content += f"    {{ s: {r['s']}, a: {r['a']} }},\n"
    js_content += "];\n\n"

print(js_content)

# Dosyaya kaydetme opsiyonu da ekleyebiliriz ama şimdilik ekrana basalım veya direkt dosyaya yazalım.
with open('isa_musa_data.js', 'w', encoding='utf-8') as f:
    f.write(js_content)
    print("isa_musa_data.js dosyası oluşturuldu.")
