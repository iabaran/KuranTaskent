"""
Scan all surah JS files for words with empty turkish translations.
"""
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

empty_words = {}
total_empty = 0
total_words = 0

for i in range(1, 115):
    filepath = os.path.join('words', f'surah_{i}.js')
    if not os.path.exists(filepath):
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    prefix = 'window.currentSurahWordData = '
    if content.startswith(prefix):
        json_str = content[len(prefix):]
        if json_str.endswith(';'):
            json_str = json_str[:-1]
        data = json.loads(json_str)
        
        for verse in data.get('verses', []):
            vn = verse['verse_number']
            for word in verse.get('words', []):
                total_words += 1
                tr = word.get('turkish', '')
                if not tr:
                    total_empty += 1
                    key = word.get('transcription', 'unknown')
                    arabic = word.get('arabic', '')
                    if key not in empty_words:
                        empty_words[key] = {'count': 0, 'arabic': arabic, 'examples': []}
                    empty_words[key]['count'] += 1
                    if len(empty_words[key]['examples']) < 3:
                        empty_words[key]['examples'].append(str(i) + ':' + str(vn))

print(f'Total words: {total_words}')
print(f'Total empty turkish: {total_empty}')
print(f'Unique transcriptions with empty: {len(empty_words)}')
print()

for k, v in sorted(empty_words.items(), key=lambda x: -x[1]['count']):
    print(f'{v["count"]:4d}x  {v["arabic"]:15s}  {k:25s}  ex: {v["examples"]}')
