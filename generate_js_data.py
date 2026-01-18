# -*- coding: utf-8 -*-
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Read the locations from files
with open('all_rahman_locations.txt', 'r', encoding='utf-8') as f:
    rahman_lines = f.readlines()

with open('all_rahim_locations.txt', 'r', encoding='utf-8') as f:
    rahim_lines = f.readlines()

# Parse Rahman locations
rahman_data = []
for line in rahman_lines:
    line = line.strip()
    if ':' in line and not line.startswith('=') and not line.startswith('-') and 'adet' not in line and 'RAHMAN' not in line and 'RAHİM' not in line and 'TÜM' not in line and 'BESMELE' not in line and 'AYET' not in line:
        parts = line.split(':')
        if len(parts) >= 2:
            try:
                s = int(parts[0])
                v = int(parts[1].split()[0])  # Remove (Besmele) if exists
                rahman_data.append({'s': s, 'a': v})
            except:
                pass

# Parse Rahim locations
rahim_data = []
for line in rahim_lines:
    line = line.strip()
    if ':' in line and not line.startswith('=') and not line.startswith('-') and 'adet' not in line and 'RAHMAN' not in line and 'RAHİM' not in line and 'TÜM' not in line and 'BESMELE' not in line and 'AYET' not in line:
        parts = line.split(':')
        if len(parts) >= 2:
            try:
                s = int(parts[0])
                v = int(parts[1].split()[0])  # Remove (Besmele) if exists
                rahim_data.append({'s': s, 'a': v})
            except:
                pass

print(f"Rahman parsed: {len(rahman_data)}")
print(f"Rahim parsed: {len(rahim_data)}")

# Generate JavaScript arrays
with open('rahman_rahim_data.js', 'w', encoding='utf-8') as f:
    f.write('// Rahman Data - 178 occurrences (113 Basmalas + 65 verses)\n')
    f.write('const rahmanData = [\n')
    for i, loc in enumerate(rahman_data):
        if i < len(rahman_data) - 1:
            f.write(f'    {{ s: {loc["s"]}, a: {loc["a"]} }},\n')
        else:
            f.write(f'    {{ s: {loc["s"]}, a: {loc["a"]} }}\n')
    f.write('];\n\n')
    
    f.write('// Rahim Data - 228 occurrences (113 Basmalas + 115 verses)\n')
    f.write('const rahimData = [\n')
    for i, loc in enumerate(rahim_data):
        if i < len(rahim_data) - 1:
            f.write(f'    {{ s: {loc["s"]}, a: {loc["a"]} }},\n')
        else:
            f.write(f'    {{ s: {loc["s"]}, a: {loc["a"]} }}\n')
    f.write('];\n')

print("\n✅ JavaScript dosyası oluşturuldu: rahman_rahim_data.js")
print(f"   - Rahman: {len(rahman_data)} adet")
print(f"   - Rahim: {len(rahim_data)} adet")
