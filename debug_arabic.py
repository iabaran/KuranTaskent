import json
with open('quran_arabic.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    text = data[0]['verses'][0]['text']
    print(f"Original: {text}")
    print(f"Hex: {' '.join(hex(ord(c)) for c in text)}")

    from analyze_19 import normalize_arabic
    norm = normalize_arabic(text)
    print(f"Normalized: {norm}")
    print(f"Norm Hex: {' '.join(hex(ord(c)) for c in norm)}")
