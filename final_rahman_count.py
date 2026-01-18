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

# Count Rahman
basmala_count = 0
basmala_surahs = []
other_rahman = []

for surah in data:
    surah_num = surah['id']
    
    # For Basmalas: check first verse of each surah (except Surah 9)
    if surah_num != 9 and len(surah['verses']) > 0:
        first_verse = surah['verses'][0]
        if first_verse['id'] == 1:
            clean_text = remove_diacritics(first_verse['text'])
            # Basmala should contain both Rahman and Rahim
            if 'رحمن' in clean_text and 'رحيم' in clean_text:
                basmala_count += 1
                basmala_surahs.append(surah_num)
    
    # Now check all verses for Rahman (excluding Basmalas)
    for verse in surah['verses']:
        verse_num = verse['id']
        text = verse['text']
        clean_text = remove_diacritics(text)
        
        # Check if Rahman exists
        if 'رحمن' in clean_text:
            # Skip if this is a Basmala we already counted
            is_basmala = (verse_num == 1 and surah_num in basmala_surahs)
            
            if not is_basmala:
                other_rahman.append((surah_num, verse_num))

print(f"📊 RAHMAN KELİMESİ ANALİZİ")
print(f"{'='*60}")
print(f"\n✅ Besmelelerdeki Rahman: {basmala_count} adet")
print(f"   (Tevbe suresi hariç tüm surelerin başındaki Besmele)")
print(f"\n✅ Besmele dışındaki Rahman: {len(other_rahman)} adet")
print(f"\n{'='*60}")
print(f"🎯 TOPLAM RAHMAN: {basmala_count + len(other_rahman)} adet")
print(f"{'='*60}")

print(f"\n📝 Detaylı Hesaplama:")
print(f"   Besmelelerde:     {basmala_count:3d} (113 sure - Tevbe hariç)")
print(f"   Diğer ayetlerde:  {len(other_rahman):3d}")
print(f"   ─────────────────────")
print(f"   TOPLAM:          {basmala_count + len(other_rahman):3d}")

print(f"\n💡 Şu anda HTML'de gösterilen: 57 (sadece Besmele dışındakiler)")
print(f"💡 Besmeleleri eklersek:       {basmala_count + len(other_rahman):3d}")

if len(other_rahman) > 0:
    print(f"\n📖 Besmele dışındaki ilk 10 Rahman:")
    for s, v in other_rahman[:10]:
        print(f"   {s}:{v}")
