#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF Sayfa -> Kuran Ayeti Eşleştirme
OCR ile sayfa çıkar, Kuran metni ile fuzzy matching yap
"""

import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import json
from pathlib import Path
from difflib import SequenceMatcher
import re

def clean_arabic_text(text):
    """Arapça metni temizle (noktalama işaretleri çıkar)"""
    # Tashkeel işaretlerini çıkar
    text = re.sub(r'[\u064B-\u065F\u0670]', '', text)
    # Fazla boşlukları temizle
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def similarity_score(text1, text2):
    """İki metin arasındaki benzerlik skorunu hesapla (0-1 arası)"""
    return SequenceMatcher(None, text1, text2).ratio()

def find_matching_verses(ocr_text, quran_data, min_similarity=0.3):
    """
    OCR metnini Kuran ayetleri ile eşleştir
    Returns: List of (surah_num, verse_num, similarity_score)
    """
    ocr_clean = clean_arabic_text(ocr_text)
    matches = []
    
    for surah_idx, surah in enumerate(quran_data):
        surah_num = surah_idx + 1
        verses = surah.get('verses', [])
        
        for verse_idx, verse in enumerate(verses):
            verse_num = verse_idx + 1
            verse_text = verse.get('text', '')
            verse_clean = clean_arabic_text(verse_text)
            
            # Benzerlik skoru hesapla
            score = similarity_score(ocr_clean, verse_clean)
            
            if score >= min_similarity:
                matches.append((surah_num, verse_num, score, verse_text))
    
    # En yüksek skora göre sırala
    matches.sort(key=lambda x: x[2], reverse=True)
    return matches

def process_pdf_page(pdf_path, page_num, quran_data):
    """Bir PDF sayfasını işle ve Kuran ayetleri ile eşleştir"""
    
    print(f"\n{'='*80}")
    print(f"SAYFA {page_num + 1} ISLENIYOR")
    print(f"{'='*80}\n")
    
    # PDF'i aç
    pdf_document = fitz.open(pdf_path)
    page = pdf_document[page_num]
    
    # Sayfayı görüntüye çevir
    zoom = 2
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)
    
    # PIL Image
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    
    # OCR uygula
    print("[*] OCR yapiliyor...")
    custom_config = r'--oem 3 --psm 6'
    ocr_text = pytesseract.image_to_string(img, lang='ara', config=custom_config).strip()
    
    print(f"[OK] OCR tamamlandi: {len(ocr_text)} karakter")
    
    pdf_document.close()
    
    if not ocr_text:
        print("[UYARI] OCR hic metin bulamadi!")
        return None
    
    # Kuran metni ile eşleştir
    print("[*] Kuran metni ile eslestiriliyor...")
    matches = find_matching_verses(ocr_text, quran_data, min_similarity=0.2)
    
    if matches:
        print(f"[OK] {len(matches)} ayet eslesmesi bulundu")
        print("\nEN IHTIMALLI ESLESME:")
        
        # En iyi 3 eşleşmeyi göster
        for i, (surah, verse, score, text) in enumerate(matches[:3], 1):
            print(f"\n  {i}. Sure {surah}, Ayet {verse}")
            print(f"     Benzerlik: %{score*100:.1f}")
        
        return matches[0]  # En iyi eşleşme
    else:
        print("[UYARI] Hicbir esleme bulunamadi!")
        return None

def main():
    """Ana program"""
    
    # PDF bul
    pdf_files = list(Path(".").glob("*Mushaf*.pdf"))
    if not pdf_files:
        print("[HATA] Mushaf PDF bulunamadi!")
        return
    
    pdf_path = str(pdf_files[0])
    
    # Kuran veritabanını yükle
    print("[*] Kuran veritabani yukleniyor...")
    with open("quran_arabic.json", "r", encoding="utf-8") as f:
        quran_data = json.load(f)
    print(f"[OK] {len(quran_data)} sure yuklendi")
    
    # 3. sayfayı test et
    page_num = 2  # 0-indexed
    result = process_pdf_page(pdf_path, page_num, quran_data)
    
    if result:
        surah, verse, score, text = result
        
        # Sonucu kaydet
        output = {
            "page_number": page_num + 1,
            "matched_surah": surah,
            "matched_verse": verse,
            "similarity_score": score,
            "verse_text": text
        }
        
        with open("page_match_result.json", "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        print(f"\n[OK] Sonuc kaydedildi: page_match_result.json")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n[HATA] {e}")
        import traceback
        traceback.print_exc()
