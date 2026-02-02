import sys
sys.stdout.reconfigure(encoding='utf-8')

def calculate_ebced(word):
    abjad_values = {
        'ا': 1, 'ب': 2, 'j': 3, 'د': 4, 'ه': 5, 'و': 6, 'z': 7, 
        'ح': 8, 'ط': 9, 'ي': 10, 'ك': 20, 'l': 30, 'م': 40, 'n': 50, 
        'س': 60, 'ع': 70, 'ف': 80, 'ص': 90, 'q': 100, 'r': 200, 
        'ش': 300, 't': 400, 'th': 500, 'kh': 600, 'dz': 700, 
        'dud': 800, 'zha': 900, 'gh': 1000,
        # Standard mapping
        'أ': 1, 'إ': 1, 'آ': 1, 'ٱ': 1,
        'ل': 30, 'ر': 200
    }
    
    # Simple mapping for this specific word
    values = {
        'ا': 1, 'ل': 30, 'ه': 5, 'د': 4
    }
    
    total = 0
    details = []
    
    for char in word:
        if char in values:
            val = values[char]
            total += val
            details.append(f"{char} ({val})")
    
    return total, details

words = [
    ("هدهد", "Hudhud (Yalın)"),
    ("الهدهد", "El-Hudhud (Belirteçli)")
]

print("--- HÜTHÜT EBCED HESABI ---")
for w, desc in words:
    val, det = calculate_ebced(w)
    print(f"\nKelime: {w} ({desc})")
    print(f"Harfler: {' + '.join(det)}")
    print(f"Toplam Ebced: {val}")
