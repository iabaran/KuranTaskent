#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Kur'an'da Gölge (ظل) kelimesini detaylı inceleyen script
"""

import json
import re

# Quran Arabic JSON dosyasını yükle
with open('quran_arabic.json', 'r', encoding='utf-8') as f:
    quran = json.load(f)

def normalize_arabic(text):
    """Harekeler ve uzatma işaretlerini kaldır"""
    diacritics = re.compile(r'[\u064B-\u065F\u0670\u06D6-\u06ED\u0640\u0653-\u0655]')
    return diacritics.sub('', text)

# Gölge kelimesi kökü: Zı-Lam (ظل)
# Hedef formlar:
# ظل (Zıll) - Gölge (Tekil)
# ظلال (Zılal) - Gölgeler (Çoğul)
# ظليل (Zalil) - Gölgeli

matches = []

print("=" * 80)
print("GÖLGE (ظل) KELİMESİ DETAYLI ANALİZİ")
print("=" * 80)

# Aranacak kelime desenleri (Normalize edilmiş)
# "Zıl" (ظل) kelimesi tek başına veya El takısı ile: الظل, ظل
# Çoğul: ظلال, الظلال
patterns = ['ظل', 'ظلال', 'ظليل', 'ظلا'] 
# Dikkat: "Zalle" (kaldı/devam etti) fiili de aynı kökten (ظل ve türevleri).
# Fiilleri elemeniz gerekebilir.
# İsim olanlar: Zıl, Zılal, Zalil.
# Fiil olanlar: Zalle, Zaltu, Zaltum, Yezallu...

# Manuel bir whitelist veya blacklist yaklaşımı daha doğru olabilir.
# Ya da basitçe listeleyip gözle kontrol edelim.

for surah in quran:
    surah_num = surah['id']
    for verse in surah['verses']:
        verse_num = verse['id']
        text = verse['text']
        normalized_text = normalize_arabic(text)
        
        words = text.split()
        for i, word in enumerate(words):
            clean_word = normalize_arabic(word)
            
            # Kök kontrolü
            if 'ظل' in clean_word:
                # Olası aday
                matches.append({
                    's': surah_num,
                    'a': verse_num,
                    'word': word,
                    'clean': clean_word
                })

print(f"{'SURE':<20} | {'AYET':<5} | {'KELİME':<15} | {'TEMİZ':<15}")
print("-" * 65)

potential_count = 0
filtered_count = 0 
final_matches = []

# Fiil olanları elemek için (Zalle/Kaldı, Devam etti anlamındaki fiiller)
# Genelde fiiller: Zalle, Zallat, Zallu, Tezallu...
# İsimler: Zıl, Zıll, Zılal, Zulel (gölgelikler)

verbs_blacklist = [
    'ظل', 'ظلت', 'ظلوا', 'فيظلل', 'فظلتم', 'تظل', 'يظل', 'لنظل', 'ظلم', 'اظلم', 'ظالم', 'مظلم'
]
# "Zulm" (Karanlık/Zulüm) kökü "Zı-Lam-Mim". "Zıl" ise "Zı-Lam".
# Yani kelimenin içinde "Mim" varsa (sonunda), genelde Zulüm köküdür.
# İstisna: "Zıl" kelimesine zamir bitişirse "Zılluhum" (onların gölgesi) -> Mim var.

for m in matches:
    w = m['clean']
    
    # 1. ZULÜM/KARANLIK Filtresi
    # Eğer "Zulm", "Zalim", "Mazlum", "Zulumat" ise ele.
    # Kök Z-L. Zulüm kökü Z-L-M.
    # Eğer kelimede M harfi kök harfi ise elenmeli.
    # "Zılluhum" -> "Zıll" + "Hum" (Zamir). Kök Z-L. Mim zamirde.
    # "Zalime" -> Kök Z-L-M.
    
    # Basit ayırt edici:
    # "ظ" ile başlar. Sonra "ل". 
    # Eğer hemen sonra "م" geliyorsa (arada elif olmadan): "Zulm" olabilir.
    # "Zulm" -> ظلم
    # "Zıll" -> ظل (son harf Lam şeddeli)
    
    is_shadow = False
    
    # İsim olan Gölge formları:
    shadow_forms = [
        'الظل', 'ظل', 'ظلا', # Tekil
        'الظلال', 'ظلال',    # Çoğul
        'ظليل', 'ظليلا',     # Sıfat (Gölgeli)
        'ظلل', 'الظلل'       # Çoğul/Gölgelikler
    ]
    
    # Ek almış halleri (ve, fe, li, bi, ke, zamirler)
    # Strateji: Kelimenin "çekirdeğini" bulmak.
    
    # Basitçe manuel pattern match yapalım, çünkü sayı az (30-40 civarı).
    
    # 1. Tam Eşleşme (Ekler hariç)
    core = w
    if core.startswith('و') or core.startswith('ف') or core.startswith('ل') or core.startswith('ب') or core.startswith('ك'):
        core = core[1:] # 1 harf at
    if core.startswith('ال'):
        core = core[2:]
    elif core.startswith('ل'): # "Lillzi..."
        pass 
        
    # En iyisi kelime kelime bakalım.
    
    # Gölge Kelimeleri Listesi (Manuel Taramadan Bilinenler)
    # 1.  4:57   zillen zalila (ظلا ظليلا) -> 2 kelime
    # 2.  ...
    
    # Otomatik filtreleme
    # Zulüm kökü (Z-L-M) içerenleri atalım
    if 'م' in w:
        # Mim var. Zamir mi kök mü?
        # Zulumat, Muzlim, Zalim -> Kök.
        # Zillehum (onların gölgesi) -> Kök Z-L.
        
        # Eğer kelime "Zulm" veya "Muzlim" ise at.
        if 'ظلم' in w or 'مظل' in w or 'ظالم' in w:
             # Zılluhum (ظلهم) içinde "ظلم" geçmez (Lam şeddeli değilse scriptte, ama text'te L-H-M sırası var).
             # Z-L-H-M. Z-L-M değil.
             pass
        elif 'ظلم' in w.replace('ل', 'lm'): # Zorlama oldu.
             pass
             
    # En temiz yöntem: İsim veritabanı veya bilinen formlar.
    # Gölge kelimeleri genelde Z-L harflerinden oluşur ve M içermez (zamir hariç).
    
    # Kesin Gölge Olanlar:
    if 'ظل' in w and not 'ظلم' in w and not 'ظالم' in w and not 'مظل' in w and not 'ظلام' in w:
         # Fiil olan Zalle (ظل) hariç tutulmalı mı?
         # Kullanıcı "Gölge" soruyor. "Zalle" (oldu/kaldı) fiili gölge demek değildir.
         # O yüzden fiilleri elemeliyiz.
         
         # Fiiller:
         # Zalle (ظل), Yezallu (يظل), Zallat (ظلت)...
         if w in ['ظل', 'ظلت', 'ظلوا', 'يظل', 'تظل', 'نظل', 'لنظل']:
             pass # Fiil
         elif w.startswith('فظل') or w.startswith('لظل'):
             pass # Fiil olma ihtimali yüksek (Fe-zalle)
         else:
             is_shadow = True
             
    # Özel Kelimeler (Zulel - Gölgelikler)
    if 'ظلل' in w:
        is_shadow = True
        
    if is_shadow:
        print(f"{m['s']:<20} | {m['a']:<5} | {m['word']:<15} | {m['clean']:<15}")
        filtered_count += 1
        final_matches.append(m)

print("-" * 65)
print(f"FİL TRELENMİŞ 'GÖLGE' SAYISI: {filtered_count}")

# JS Data formatı
js_content = "const zilData = [\n"
for m in final_matches:
    js_content += f"    {{ s: {m['s']}, a: {m['a']}, w: \"{m['word']}\" }},\n"
js_content += "];"

print("\n")
# print(js_content)

with open('zil_data.js', 'w', encoding='utf-8') as f:
    f.write(js_content)
    
