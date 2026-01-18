import json
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('angel_satan_data.js', 'r', encoding='utf-8') as f:
    content = f.read()
    # Extract json part for angelData
    # Look for [ ... ];
    start = content.find('const angelData = [')
    if start == -1:
        print("Could not find angelData start")
        sys.exit(1)
    
    start += len('const angelData = ')
    end = content.find('];', start) + 1
    json_str = content[start:end]
    data = json.loads(json_str)
    print(f"Loaded {len(data)} items")

with open('quran_arabic.json', 'r', encoding='utf-8') as f:
    quran = json.load(f)

forms = {}
for item in data:
    s = item['s']
    a = item['a']
    text = quran[s-1]['verses'][a-1]['text']
    # Find the word in text
    # This is tricky without knowing which word was matched.
    # But we can look for 'mlk' words.
    words = text.split()
    if len(forms) == 0:
        print(f"Sample Text ({s}:{a}): {text}")
        
    for w in words:
        # Just print any word resembling angel root to see what we have
        # Normalized check
        if 'ملائك' in w or 'ملك' in w:
             if w not in forms: forms[w] = 0
             forms[w] += 1

print("Found Angel Forms:")
for f, c in sorted(forms.items(), key=lambda x: x[1], reverse=True):
    print(f"{f}: {c}")
