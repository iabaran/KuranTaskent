
# -*- coding: utf-8 -*-
import json
import sys

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

jannah_data = [{"s": 2, "a": 35, "w": "الجنة"}, {"s": 2, "a": 82, "w": "الجنة"}, {"s": 2, "a": 111, "w": "الجنة"}, {"s": 2, "a": 214, "w": "الجنة"}, {"s": 2, "a": 221, "w": "الجنة"}, {"s": 2, "a": 265, "w": "جنة"}, {"s": 2, "a": 266, "w": "جنة"}, {"s": 3, "a": 133, "w": "وجنة"}, {"s": 3, "a": 142, "w": "الجنة"}, {"s": 3, "a": 185, "w": "الجنة"}, {"s": 4, "a": 124, "w": "الجنة"}, {"s": 5, "a": 72, "w": "الجنة"}, {"s": 7, "a": 19, "w": "الجنة"}, {"s": 7, "a": 22, "w": "الجنة"}, {"s": 7, "a": 27, "w": "الجنة"}, {"s": 7, "a": 40, "w": "الجنة"}, {"s": 7, "a": 42, "w": "الجنة"}, {"s": 7, "a": 43, "w": "الجنة"}, {"s": 7, "a": 44, "w": "الجنة"}, {"s": 7, "a": 46, "w": "الجنة"}, {"s": 7, "a": 49, "w": "الجنة"}, {"s": 7, "a": 50, "w": "الجنة"}, {"s": 9, "a": 111, "w": "الجنة"}, {"s": 10, "a": 26, "w": "الجنة"}, {"s": 11, "a": 23, "w": "الجنة"}, {"s": 11, "a": 108, "w": "الجنة"}, {"s": 13, "a": 35, "w": "الجنة"}, {"s": 16, "a": 32, "w": "الجنة"}, {"s": 17, "a": 91, "w": "جنة"}, {"s": 18, "a": 32, "w": "جنتين"}, {"s": 18, "a": 33, "w": "الجنتين"}, {"s": 18, "a": 35, "w": "جنته"}, {"s": 18, "a": 39, "w": "جنتك"}, {"s": 18, "a": 40, "w": "جنتك"}, {"s": 19, "a": 60, "w": "الجنة"}, {"s": 19, "a": 63, "w": "الجنة"}, {"s": 20, "a": 117, "w": "الجنة"}, {"s": 20, "a": 121, "w": "الجنة"}, {"s": 25, "a": 8, "w": "جنة"}, {"s": 25, "a": 15, "w": "جنة"}, {"s": 25, "a": 24, "w": "الجنة"}, {"s": 26, "a": 85, "w": "جنة"}, {"s": 26, "a": 90, "w": "الجنة"}, {"s": 29, "a": 58, "w": "الجنة"}, {"s": 34, "a": 15, "w": "جنتان"}, {"s": 34, "a": 16, "w": "بجنتيهم"}, {"s": 34, "a": 16, "w": "جنتين"}, {"s": 36, "a": 26, "w": "الجنة"}, {"s": 36, "a": 55, "w": "الجنة"}, {"s": 39, "a": 73, "w": "الجنة"}, {"s": 39, "a": 74, "w": "الجنة"}, {"s": 40, "a": 40, "w": "الجنة"}, {"s": 41, "a": 30, "w": "بالجنة"}, {"s": 42, "a": 7, "w": "الجنة"}, {"s": 43, "a": 70, "w": "الجنة"}, {"s": 43, "a": 72, "w": "الجنة"}, {"s": 46, "a": 14, "w": "الجنة"}, {"s": 46, "a": 16, "w": "الجنة"}, {"s": 47, "a": 6, "w": "الجنة"}, {"s": 47, "a": 15, "w": "الجنة"}, {"s": 50, "a": 31, "w": "الجنة"}, {"s": 53, "a": 15, "w": "جنة"}, {"s": 55, "a": 46, "w": "جنتان"}, {"s": 55, "a": 54, "w": "الجنتين"}, {"s": 55, "a": 62, "w": "جنتان"}, {"s": 56, "a": 89, "w": "وجنت"}, {"s": 57, "a": 21, "w": "وجنة"}, {"s": 58, "a": 16, "w": "جنة"}, {"s": 59, "a": 20, "w": "الجنة"}, {"s": 59, "a": 20, "w": "الجنة"}, {"s": 63, "a": 2, "w": "جنة"}, {"s": 66, "a": 11, "w": "الجنة"}, {"s": 68, "a": 17, "w": "الجنة"}, {"s": 69, "a": 22, "w": "جنة"}, {"s": 70, "a": 38, "w": "جنة"}, {"s": 76, "a": 12, "w": "جنة"}, {"s": 79, "a": 41, "w": "الجنة"}, {"s": 81, "a": 13, "w": "الجنة"}, {"s": 88, "a": 10, "w": "جنة"}, {"s": 89, "a": 30, "w": "جنتي"}]

print(f"Total entries: {len(jannah_data)}")

counts = {}
for item in jannah_data:
    w = item["w"]
    counts[w] = counts.get(w, 0) + 1

print("\nWord Frequency:")
for w, c in sorted(counts.items(), key=lambda x: x[1], reverse=True):
    print(f"{w}: {c}")

print("\nEntries with potential 'non-standard' forms (Dual/Possessive/Plural-ish):")
potential_exclusions = []
for item in jannah_data:
    w = item["w"]
    # Check for dual endings (an, ayn) or possessive suffixes (hu, ka, i) or distinct forms
    # Standard: الجنة (Al-Jannah), جنة (Jannah), وجنة (Wa-Jannah), بالجنة (Bi-al-Jannah)
    # Suspect: جنتين, الجنتين, جنتان, بجنتيهم, وجنت, جنتي, جنته, جنتك
    
    is_standard = w in ["الجنة", "جنة", "وجنة", "بالجنة"]
    if not is_standard:
        print(f"{item['s']}:{item['a']} - {w}")
        potential_exclusions.append(item)

print(f"\nNon-standard count: {len(potential_exclusions)}")
print(f"Standard count: {len(jannah_data) - len(potential_exclusions)}")
print(f"Target count: 80 - {len(potential_exclusions)} = {len(jannah_data) - len(potential_exclusions)}")

# Also checking 'Earthly' verses context manually in code comment
# 2:265 (Garden on high ground)
# 2:266 (Garden of palms)
# 18:32-40 (Man with two gardens)
# 17:91 (Your garden of palms - earthly)
# 25:8 (Garden - earthly rhetorical)
# 34:15-16 (Saba gardens)
# 68:17 (People of the garden)

earthly_verses = [
    (2, 265), (2, 266), 
    (17, 91),
    (18, 32), (18, 33), (18, 35), (18, 39), (18, 40),
    (25, 8),
    (34, 15), (34, 16),
    (68, 17)
]

print("\nChecking known 'Earthly' references in list:")
earthly_hits = []
for item in jannah_data:
    if (item['s'], item['a']) in earthly_verses:
        print(f"Earthly? {item['s']}:{item['a']} - {item['w']}")
        earthly_hits.append(item)

print(f"Total Earthly References found: {len(earthly_hits)}")
