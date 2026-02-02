import sys
sys.stdout.reconfigure(encoding='utf-8')

def calculate_ebced(word):
    # Abjad values (Standard/Eastern)
    abjad_values = {
        'ا': 1, 'ب': 2, 'ج': 3, 'د': 4, 'ه': 5, 'و': 6, 'ز': 7, 
        'ح': 8, 'ط': 9, 'ي': 10, 'ك': 20, 'ل': 30, 'م': 40, 'n': 50, 
        'س': 60, 'ع': 70, 'ف': 80, 'ص': 90, 'ق': 100, 'r': 200, 
        'ش': 300, 'ت': 400, 'th': 500, 'kh': 600, 'dz': 700, 
        'dud': 800, 'zha': 900, 'gh': 1000,
        'ر': 200 # Ra
    }
    
    total = 0
    details = []
    
    for char in word:
        if char in abjad_values:
            val = abjad_values[char]
            total += val
            details.append(f"{char} ({val})")
            
    return total, details

word = "سقر" # Sakar
val, det = calculate_ebced(word)

print("--- SAKAR EBCED HESABI ---")
print(f"Kelime: {word}")
print(f"Harfler: {' + '.join(det)}")
print(f"Toplam: {val}")
