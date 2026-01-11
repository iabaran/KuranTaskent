#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
3. Sayfa İlk Satır - Tesseract OCR Testi (Tamamen Ücretsiz)
"""

import fitz  # PyMuPDF
from PIL import Image
import pytesseract
from pathlib import Path
import sys

def test_first_line_tesseract():
    """3. sayfanın ilk satırını Tesseract ile OCR yapar"""
    
    # PDF dosyasını bul
    pdf_files = list(Path(".").glob("*Mushaf*.pdf"))
    
    if not pdf_files:
        print("[HATA] Mushaf PDF dosyasi bulunamadi!")
        return
    
    pdf_path = str(pdf_files[0])
    
    print("=" * 80)
    print("3. SAYFA ILK SATIR TESTI - TESSERACT OCR (UCRETSIZ)")
    print("=" * 80)
    print()
    
    # PDF'i aç
    print(f"[*] PDF aciliyor: {pdf_path}")
    pdf_document = fitz.open(pdf_path)
    
    # 3. sayfayı al (index 2)
    page_num = 2
    page = pdf_document[page_num]
    
    # Sayfayı yüksek çözünürlükte görüntüye çevir
    print(f"[*] Sayfa {page_num + 1} goruntuye donusturuluyor...")
    zoom = 3  # Yüksek kalite
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)
    
    # PIL Image'e dönüştür
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    width, height = img.size
    
    # Sayfanın üst %15'lik kısmını al (ilk satırlar için)
    crop_box = (0, 0, width, int(height * 0.15))
    cropped_img = img.crop(crop_box)
    
    print(f"    Goruntu boyutu: {width}x{height}")
    print(f"    Kirpilmis bolge: {cropped_img.size[0]}x{cropped_img.size[1]} (ust %15)")
    
    # Görüntüyü kaydet
    output_img = "test_3_sayfa_tesseract.png"
    cropped_img.save(output_img)
    print(f"[*] Test edilen bolge kaydedildi: {output_img}")
    
    # Tesseract OCR
    print("\n[*] Tesseract OCR islemi yapiliyor (Arapca)...")
    
    # Tesseract ayarları
    custom_config = r'--oem 3 --psm 6'  # LSTM engine, tek metin bloğu
    
    try:
        arabic_text = pytesseract.image_to_string(
            cropped_img, 
            lang='ara',
            config=custom_config
        ).strip()
    except Exception as e:
        print(f"[HATA] Tesseract OCR hatasi: {e}")
        return
    
    print("\n" + "=" * 80)
    print("SONUCLAR:")
    print("=" * 80)
    
    if not arabic_text:
        print("\n[UYARI] OCR hic metin bulamadi!")
        print(f"Lutfen {output_img} dosyasini kontrol edin.")
        print("\nOlasi nedenler:")
        print("- Goruntu kalitesi dusuk olabilir")
        print("- El yazisi Tesseract icin zor olabilir")
        print("- Arapca dil dosyasi (ara) kurulu olmayabilir")
    else:
        # İstatistikler
        kelime_sayisi = len(arabic_text.split())
        satir_sayisi = len(arabic_text.split('\n'))
        
        print(f"\n[OK] OCR BASARILI!")
        print("\nISTATISTIKLER:")
        print(f"   Karakter: {len(arabic_text)}")
        print(f"   Kelime: {kelime_sayisi}")
        print(f"   Satir: {satir_sayisi}")
        print("\n   Not: Arapca metin dosyaya kaydedildi (konsol encoding sorunu)")
    
    # Sonuçları dosyaya kaydet
    output_txt = "test_3_sayfa_tesseract_sonuc.txt"
    with open(output_txt, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("3. SAYFA ILK SATIR - TESSERACT OCR SONUCU (UCRETSIZ)\n")
        f.write("=" * 80 + "\n\n")
        f.write("ARAPCA METIN:\n")
        f.write("-" * 80 + "\n")
        f.write(arabic_text if arabic_text else "[Metin bulunamadi]")
        f.write("\n")
    
    print(f"\n[OK] Sonuclar kaydedildi: {output_txt}")
    print(f"[OK] Goruntu kaydedildi: {output_img}")
    print("\n" + "=" * 80)
    print("Test tamamlandi! (Tamamen ucretsiz)")
    print("=" * 80)
    
    pdf_document.close()

if __name__ == "__main__":
    try:
        test_first_line_tesseract()
    except Exception as e:
        print(f"\n[HATA] {e}")
        import traceback
        traceback.print_exc()
