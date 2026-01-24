import re

# quran_tr_js.js dosyasını oku ve Sad suresini (38) kontrol et
with open('quran_tr_js.js', 'r', encoding='utf-8') as f:
    content = f.read()

# QURAN_TR array'ini bul
# Format: const QURAN_TR = [ ... ]
# Her sure bir array, her ayet bir string

# Regex ile 38. sureyi bul (index 37)
# Önce dosyanın yapısını görelim
lines = content.split('\n')
for i, line in enumerate(lines[:50]):  # İlk 50 satırı göster
    print(f"Line {i+1}: {line[:100]}")

print("\n=== Sad suresi aranıyor (index 37) ===\n")

# Sad suresini bul
in_surah_38 = False
verse_count = 0
for i, line in enumerate(lines):
    if '"38:' in line or "'38:" in line:
        print(f"Line {i+1}: {line.strip()[:150]}")
        verse_count += 1
        if verse_count >= 5:  # İlk 5 ayeti göster
            break
