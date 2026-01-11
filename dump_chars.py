import json
import collections
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def dump_chars():
    with open('quran_arabic.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    baqara = data[1]
    
    counts = collections.Counter()
    for v in baqara['verses']:
        counts.update(v['text'])
        
    print(f"{'Char':<5} | {'Hex':<8} | {'Count':<8}")
    print("-" * 25)
    for char, count in counts.most_common():
        print(f"{char:<5} | {hex(ord(char)):<8} | {count:<8}")

if __name__ == "__main__":
    dump_chars()
