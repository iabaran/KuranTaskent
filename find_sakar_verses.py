import json
import re

file_path = r"d:\KuranTaskent\quran_tr_js.js"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# The file looks like: const GLOBAL_QURAN_TR = { ... };
# We need to extract the JSON part.
match = re.search(r"const GLOBAL_QURAN_TR = (.*);", content, re.DOTALL)
if not match:
    # Maybe it doesn't have a semicolon at the end or it's slightly different
    match = re.search(r"const GLOBAL_QURAN_TR = (.*)", content, re.DOTALL)

if match:
    json_str = match.group(1).strip()
    # If it ends with a semicolon, remove it
    if json_str.endswith(";"):
        json_str = json_str[:-1].strip()
    
    try:
        data = json.loads(json_str)
        s74 = data.get("74")
        if s74:
            print("Surah 74 found!")
            for i in range(26, 31):
                a = str(i)
                print(f"Verse {a}: {s74['ayahs'].get(a)}")
        else:
            print("Surah 74 NOT found in data.")
    except Exception as e:
        print(f"Error parsing JSON: {e}")
else:
    print("Could not find GLOBAL_QURAN_TR variable in file.")
