import json

# Arapça verileri kontrol et
with open('quran_arabic.json', 'r', encoding='utf-8') as f:
    arabic_data = json.load(f)

print("=== ARAPÇA VERİLER ===")
print(f"38:1 Arabic: {arabic_data[37][0]}")  # 0-indexed
print(f"38:2 Arabic: {arabic_data[37][1]}")
print()

# Türkçe çeviriyi kontrol et - quran_tr_js.js dosyasını kontrol etmeliyiz
# Ama önce JSON formatında mı yoksa JS formatında mı bakalım
try:
    with open('quran_tr.json', 'r', encoding='utf-8') as f:
        tr_data = json.load(f)
    print("=== TÜRKÇE VERİLER (JSON) ===")
    print(f"38:1 Turkish: {tr_data[37][0]}")
    print(f"38:2 Turkish: {tr_data[37][1]}")
except FileNotFoundError:
    print("quran_tr.json bulunamadı, JS dosyasını kontrol etmeliyiz")
