import json
import re
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def normalize_custom(text):
    # Remove all diacritics
    noise = re.compile(r'[\u0610-\u061A\u064B-\u065F\u06D6-\u06ED\u08E4-\u08FE\u0670\u0671]')
    return re.sub(noise, '', text)

def analyze_fatiha_deep():
    with open('quran_arabic.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    fatiha = data[0]
    
    # 1. Hemze ve Sakin Elif (30 defa)
    # Sakin elif usually means Elif without vowels or just the count of Elifs.
    # Hamzas: ء أ ؤ إ ئ
    
    hamzas = re.compile(r'[\u0621\u0622\u0623\u0624\u0625\u0626]')
    alifs = re.compile(r'\u0627')
    lams = re.compile(r'\u0644')
    mims = re.compile(r'\u0645')
    
    full_text_with_b = " ".join(v['text'] for v in fatiha['verses'])
    text_no_b = " ".join(v['text'] for v in fatiha['verses'][1:]) # V2 to V7
    
    # Counts with Basmala
    h_count = len(hamzas.findall(full_text_with_b))
    a_count = len(alifs.findall(full_text_with_b))
    l_count = len(lams.findall(full_text_with_b))
    m_count = len(mims.findall(full_text_with_b))
    
    # Counts without Basmala (V2-V7)
    a_count_no_b = len(alifs.findall(text_no_b))
    l_count_no_b = len(lams.findall(text_no_b))
    
    # "Elif-lam (ال)" count: 13
    al_count = len(re.findall(r'\u0627\u0644', full_text_with_b))
    
    print(f"Fatiha Deep Analysis Results:")
    print(f"1. Hamza Count (full): {h_count}")
    print(f"2. Alif Count (full): {a_count}")
    print(f"   Sum (H + A): {h_count + a_count}")
    print(f"3. Lam Count (full): {l_count}")
    print(f"   Lam Count (no Besmele): {l_count_no_b}")
    print(f"4. Alif + Lam (no Besmele): {a_count_no_b + l_count_no_b}")
    print(f"5. Mim Count (full): {m_count}")
    print(f"6. Elif-Lam (ال) Count: {al_count}")

if __name__ == "__main__":
    analyze_fatiha_deep()
