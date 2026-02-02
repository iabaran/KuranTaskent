import re

def count_in_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Common words used for Rahim/Rahman in Turkish
    words = [
        "Rahim", "Rahman", "Bağışlayan", "Esirgeyen", "merhametli", "merhamet"
    ]
    
    results = {}
    for w in words:
        # Case insensitive count
        count = len(re.findall(re.escape(w), content, re.IGNORECASE))
        results[w] = count
        
    return results

file_path = 'd:/KuranTaskent/quran_tr_js.js'
res = count_in_file(file_path)
for w, c in res.items():
    print(f"{w}: {c}")
