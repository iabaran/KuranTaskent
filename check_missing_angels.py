import json

# Check for specific known Angel verses
known_singular = [
    (6, 8), (6, 9), (6, 9), # 6:9 has two? "laja'alnahu malakan wa laja'alna..." ?
    (6, 50), (6, 111), (6, 158), # 6:50 "Inni malakun".
    (11, 12), (11, 31),
    (12, 31),
    (15, 7), (15, 8),
    (16, 2), # Malaika?
    (17, 95), (17, 95), # Two in 95? "Malakan rasulan"
    (23, 24),
    (25, 7), (25, 21),
    (32, 11),
    (33, 43), # Malaika plural
    (41, 14), (41, 30),
    (43, 53),
    (47, 27),
    (53, 26),
    (66, 4), (66, 6),
    (69, 17), # "Wal-Malaku" (The Angel/Angels collective?) 69:17.
    (70, 4),
    (89, 22), # "Wal-Malaku saffan saffan"
    (97, 4)
]

with open('angel_satan_data.js', 'r', encoding='utf-8') as f:
    content = f.read()
    start = content.find('const angelData = [')
    start += len('const angelData = ')
    end = content.find('];', start) + 1
    data = json.loads(content[start:end])

found_set = set()
for x in data:
    found_set.add((x['s'], x['a']))

print("Missing Known Verses:")
for s, a in known_singular:
    if (s, a) not in found_set:
        print(f"Missing {s}:{a}")
    else:
        # print(f"Found {s}:{a}")
        pass
        
print(f"Total Found in Data: {len(data)}")
