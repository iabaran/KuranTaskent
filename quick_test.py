#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hızlı OCR Testi - 1 Sayfa, 1 Satır
"""

import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io

def quick_ocr_test():
    """PDF'nin ilk sayfasından küçük bir bölge alıp OCR test eder"""
    
    # PDF dosyasını dinamik olarak bul
    from pathlib import Path
    pdf_files = list(Path(".").glob("*Mushaf*.pdf"))
    
    if not pdf_files:
        print("[HATA] Mushaf PDF dosyasi bulunamadi!")
        return
    
    pdf_path = str(pdf_files[0])
    
    print("=" * 80)
    print("HIZLI OCR TESTI")
    print("=" * 80)
    print()
    
    # PDF'i ac
    print(f"[*] PDF aciliyor: {pdf_path}")
    pdf_document = fitz.open(pdf_path)
    total_pages = len(pdf_document)
    print(f"    Toplam sayfa sayisi: {total_pages}")
    print()
    
    # 3. sayfayi al (sayfa 2)
    page_num = 2  # 0-indexed: 0=sayfa1, 1=sayfa2, 2=sayfa3
    page = pdf_document[page_num]
    
    # Sayfayi yuksek cozunurlukle goruntuye cevir
    print(f"[*] Sayfa {page_num + 1} goruntuye donusturuluyor...")
    zoom = 2  # Daha iyi OCR icin yuksek cozunurluk
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)
    
    # PIL Image'e donustur
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    
    # Sayfanin ust kismindan kucuk bir bolge al (ilk satirlar icin)
    # Genellikle Arapca metinler sagdan sola ve yukaridan asagiya yazilir
    width, height = img.size
    
    # Ust %20'lik kismi al (baslik ve ilk satirlar)
    crop_box = (0, 0, width, int(height * 0.2))
    cropped_img = img.crop(crop_box)
    
    print(f"    Goruntu boyutu: {width}x{height}")
    print(f"    Kirpilmis bolge: {cropped_img.size[0]}x{cropped_img.size[1]} (ust %20)")
    print()
    
    # OCR uygula
    print("[*] OCR islemi yapiliyor (Arapca)...")
    custom_config = r'--oem 3 --psm 6'  # LSTM OCR Engine, tek duz metin blogu varsay
    text = pytesseract.image_to_string(cropped_img, lang='ara', config=custom_config)
    
    print()
    print("=" * 80)
    print("SONUC:")
    print("=" * 80)
    print()
    
    # Metni dosyaya kaydet (konsol kodlama problemi nedeniyle)
    output_txt = "ocr_test_sonuc.txt"
    with open(output_txt, 'w', encoding='utf-8') as f:
        f.write(text)
    
    print(f"[OK] OCR sonucu kaydedildi: {output_txt}")
    print(f"[OK] Toplam {len(text)} karakter tanindi")
    print(f"[OK] Toplam {len(text.split())} kelime tanindi")
    print()
    print("=" * 80)
    
    # Kirpilmis goruntuyu kaydet
    output_img = "test_bolge.png"
    cropped_img.save(output_img)
    print(f"[*] Test edilen bolge goruntusu: {output_img}")
    
    pdf_document.close()
    
    
    # Ek bilgi
    print()
    print("KONTROL:")
    print(f"1. {output_txt} dosyasini acarak OCR kalitesini inceleyin")
    print(f"2. {output_img} dosyasini acarak hangi bolgenin test edildigini gorun")
    print()

if __name__ == "__main__":
    try:
        quick_ocr_test()
    except Exception as e:
        print(f"\n[HATA] {e}")
        import traceback
        traceback.print_exc()
