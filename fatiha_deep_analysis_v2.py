import json
import re
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def analyze_fatiha_refined():
    with open('quran_arabic.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    fatiha = data[0]
    
    # Character Patterns
    # Alifs: regular (ا), wasla (ٱ), madda (آ), hamza types (أ إ)
    alifs_pattern = re.compile(r'[\u0627\u0671\u0622\u0623\u0625]')
    hamza_isolated = re.compile(r'\u0621')
    lams_pattern = re.compile(r'\u0644')
    mims_pattern = re.compile(r'\u0645')
    
    # Elif-Lam (Definite article) - Usually starts with Alif/Wasla followed by Lam
    al_pattern = re.compile(r'[\u0627\u0671][\u0644]')
    
    full_text = " ".join(v['text'] for v in fatiha['verses'])
    text_no_b = " ".join(v['text'] for v in fatiha['verses'][1:]) # V2 to V7
    
    # Global Counts
    a_total = len(alifs_pattern.findall(full_text))
    h_total = len(hamza_isolated.findall(full_text))
    l_total = len(lams_pattern.findall(full_text))
    m_total = len(mims_pattern.findall(full_text))
    al_total = len(al_pattern.findall(full_text))
    
    # Without Basmala
    a_no_b = len(alifs_pattern.findall(text_no_b))
    l_no_b = len(lams_pattern.findall(text_no_b))
    
    print(f"Refined Fatiha Analysis:")
    print(f"Alifs (All types): {a_total}")
    print(f"Hamzas (Isolated): {h_total}")
    print(f"Lams (All): {l_total}")
    print(f"Mims (All): {m_total}")
    print(f"Elif-Lam (Definite Article): {al_total}")
    print(f"Lams (Without Basmala): {l_no_b}")
    print(f"Alifs + Lams (Without Basmala): {a_no_b + l_no_b}")
    
    # Check "Hemze + Sakin Elif = 30"
    # Sakin Elif usually means the "Alif" form.
    print(f"Hemze forms (أ إ ء) + Alif forms (ا آ ٱ): {a_total + h_total}")

if __name__ == "__main__":
    analyze_fatiha_refined()
