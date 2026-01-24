#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Kur'an'da Adem (آدم) kelimesini daha kapsamlı sayan script (V2)
"""

import json
import re

# Quran Arabic JSON dosyasını yükle
with open('quran_arabic.json', 'r', encoding='utf-8') as f:
    quran = json.load(f)

def full_normalize(text):
    """
    Sadece harekeleri değil, Elif ve Hemze varyasyonlarını da normalize eder.
    Böylece arama daha esnek olur.
    """
    # 1. Harekeleri kaldır
    # \u064B-\u065F: Tanwinler, Fatha, Damma, Kasra, Shadda, Sukun
    # \u0670: Superscript Alef
    # \u06D6-\u06ED: Kuran durak işaretleri vb.
    # \u0640: Tatweel (uzatma çizgisi)
    text = re.sub(r'[\u064B-\u065F\u0670\u06D6-\u06ED\u0640\u0653-\u0655]', '', text)
    
    # 2. Elif varyasyonlarını 'ا' (Normal Elif) yap
    # \u0622: Alif with Madda (آ)
    # \u0623: Alif with Hamza Above (أ)
    # \u0625: Alif with Hamza Below (إ)
    # \u0671: Alif Wasla (ٱ)
    text = re.sub(r'[آأإٱ]', 'ا', text)
    
    # 3. Hemze varyasyonlarını 'ء' yap (vav üstü, ya üstü vb.)
    # \u0624: Waw with Hamza (ؤ)
    # \u0626: Yeh with Hamza (ئ)
    text = re.sub(r'[ؤئ]', 'ء', text)
    
    return text

# Hedef kelime "Adem"
# Normalize edilmiş hali: "ااد" (Alif Alif Dal Mim) -> Çünkü 'آ' -> 'ا' yapılırsa ve 'ء' -> 'ء' kalırsa
# Standart Adem: 'آدم' -> Normalize: 'ادم' (Elif Dal Mim)
# Beklenen varyasyonlar:
# 1. 'آدم' (AlifMadda + Dal + Mim) -> Normalize: 'ادم'
# 2. 'ءادم' (Hemze + Elif + Dal + Mim) -> Normalize: 'ءادم'
# 3. 'أدم' (AlifHamza + Dal + Mim) -> Normalize: 'ادم'
#
# En iyisi, normalize fonksiyonunu kullanarak hedef pattern'i belirlemek değil, 
# Adem sesini veren kökleri regex ile aramak.

# Kuran'daki Adem yazımı genelde: ء ا د م (Hemze, Elif, Dal, Mim) veya آ د م
# "Ey Adem" -> "يَـَٔادَمُ" -> Y-Hemze-A-D-M

# Strateji: Kelimenin içinde "dm" (Dal-Mim) geçip, önünde "A" sesi olanları bulup listeleyelim,
# sonra manuel kontrol edelim (zaten 25 tane olması lazım).

potential_matches = []

for surah in quran:
    surah_num = surah['id']
    surah_name = surah.get('name', f'Sure {surah_num}')
    
    for verse in surah['verses']:
        verse_num = verse['id']
        text = verse['text']
        
        # Kelimelere ayır
        words = text.split()
        
        for word in words:
            # Temizle
            clean_word = full_normalize(word)
            
            # İçinde "دم" (dm) geçiyor mu? (Adem'in sonu)
            if 'دم' in clean_word:
                # Önünde Elif veya Hemze var mı?
                # Olası Adem formları: ادم, ءادم, يادم (Ya Adem)
                if 'ادم' in clean_word or 'ءادم' in clean_word:
                     # Negatif filtre (Adem olmayan ama benzeyenler)
                     # "Nadem" (pişmanlık), "Ledem" vb. varsa elemek lazım ama Kuran'da "Nadem" var mı bu kökten?
                     # "Dem" (kan) kelimesi var mı? "Demin" (sonra) vb.
                     
                     # Basitçe ekle, kullanıcıya göstermeden önce biz süzeriz.
                     # Amaç 25 sayısını bulmak.
                     potential_matches.append({
                        's': surah_num, 
                        'a': verse_num, 
                        'word': word,
                        'clean': clean_word
                     })

print(f"Toplam aday kelime sayısı: {len(potential_matches)}")

# Adayları gruplayıp sayalım
adem_occurences = []
total_adem = 0

print("\n--- BULUNAN 'ADEM' ADAYLARI ---")
for pm in potential_matches:
    w = pm['clean']
    # Kesin Adem Kontrolleri
    is_adem = False
    
    # 1. Tam 'ادم' veya 'الادم' (El-Adem)
    if w == 'ادم' or w == 'الادم': 
        is_adem = True
    
    # 2. 'ءادم' (Hemze-Elif-Dal-Mim)
    elif 'ءادم' in w:
        is_adem = True
        
    # 3. 'يادم' (Ya Adem - birleşik) - Normalize edilince 'ياادم' veya 'يادم' olabilir
    elif w.endswith('ادم') and ('يا' in w or 'ل' in w or 'بني' in w or 'و' in w or 'ف' in w):
         # "Ve Adem", "Fe Adem", "Li Adem", "Beni Adem"
         is_adem = True
         
    # Hatalı pozitif eleme
    # "Dem" (Kan): 'دم' -> Normalize 'دم'. "Ed-dem" -> 'الدم'. Bunlar 'ادم' değil.
    # "Nedem" (Pişmanlık): 'ندم'.
    # "Adem" kelimesinin "Dal" harfi genelde 2. veya 3. harf köküdür.
    
    if is_adem:
        # Tekrar kontrol: Sadece 25 tane olmalı
        # Zaten listeye ekleyelim.
        # Aynı ayette birden fazla olabilir mi? Evet.
        
        # Listeyi benzersizleştirmek yerine her geçişi sayacağız.
        print(f"Sure {pm['s']}:{pm['a']} - {pm['word']} (Clean: {w})")
        adem_occurences.append(pm)
        total_adem += 1

print(f"\nToplam filtrelenmiş 'Adem' sayısı: {total_adem}")

# Eğer 25 ise JS oluşturalım
if total_adem == 25:
    print("\n✅ MÜKEMMEL! 25 ADET BULUNDU (19 SİSTEMİNE UYGUN)")
    
    js_output = "const ademData = [\n"
    seen_verses = set() # Aynı ayette 2 kere geçiyorsa? Adem genelde ayet başına 1 kere geçer ama kontrol edelim.
    # Kuran okuyucuda her kelimeyi vurgulamak istiyorsak, tüm geçişleri vermeliyiz.
    # Ancak tooltip yapım ayet bazlı (highlightWord tüm ayette çalışıyor).
    # O yüzden unique verses yeterli olabilir mi? Hayır, count 25 ise, 25 satır olmalı listede (eğer ayet tekrar ediyorsa).
    # Ama mevcut yapım ayet başına 1 satır gösteriyor.
    # Adem kelimesi aynı ayette 2 kere geçer mi?
    # Bakara 33: "Ya Adem... Adem..." -> 2 kere geçebilir.
    # Bakara 35: ...
    # Bakara 37: ...
    
    # Listem ayet referanslı. Eğer bir ayette 2 kere geçiyorsa ve toplam 25 ise, listede 25 satır olmalı mı?
    # Adem (15) + İsa (25) + Musa (136) listesi "Ayet Listesi" mi yoksa "Kelime Listesi" mi?
    # Benim JS formatı `[{s:2, a:31}, ...]` şeklinde.
    # Eğer aynı ayette 2 kere geçiyorsa, JS'e 2 kere eklesem de arayüzde 1 kere görünür (unique key sorunu olmazsa).
    # Ancak tooltipte liste olarak döküldüğünde 2 satır görünürse "Bakara 35" ve "Bakara 35" diye, saçma olabilir.
    # Ama sayı 25 ise ve 25 madde varsa doğru olan budur.
    
    # Gruplama
    # Ayet numarasına göre sırala
    # adem_occurences.sort(...) 
    pass # Script çalışınca göreceğiz.
else:
    print(f"\n⚠️ DİKKAT: Sayı 25 değil ({total_adem}). İnceleme gerekiyor.")
