#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
3. Sayfa İlk Satır OCR Testi - Sadece Vision API (Çeviri YOK)
Aylık 1000 OCR ücretsiz
"""

import fitz  # PyMuPDF
from google.cloud import vision
from PIL import Image
import io
import os
from pathlib import Path
from dotenv import load_dotenv

def test_vision_only():
    """3. sayfanın ilk satırını sadece OCR yapar (çeviri yok)"""
    
    # .env dosyasını yükle
    load_dotenv()
    
    # PDF dosyasını bul
    pdf_files = list(Path(".").glob("*Mushaf*.pdf"))
    
    if not pdf_files:
        print("[HATA] Mushaf PDF dosyasi bulunamadi!")
        return
    
    pdf_path = str(pdf_files[0])
    
    print("=" * 80)
    print("3. SAYFA ILK SATIR - GOOGLE VISION OCR TESTI")
    print("(Ceviri YOK - Sadece OCR, Aylik 1000 ucretsiz)")
    print("=" * 80)
    print()
    
    # Google Cloud Vision client oluştur
    try:
        vision_client = vision.ImageAnnotatorClient()
        print("[OK] Google Cloud Vision baglantisi basarili")
    except Exception as e:
        print(f"[HATA] Google Cloud baglantisi kurulamadi: {e}")
        print("\nLutfen .env dosyasinda GOOGLE_APPLICATION_CREDENTIALS ayarlanmis mi kontrol edin.")
        print("Veya .agent/workflows/setup-google-credentials.md dosyasina bakin.")
        return
    
    # PDF'i aç
    print(f"\n[*] PDF aciliyor: {pdf_path}")
    pdf_document = fitz.open(pdf_path)
    
    # 3. sayfayı al (index 2)
    page_num = 2
    page = pdf_document[page_num]
    
    # Sayfayı yüksek çözünürlükte görüntüye çevir
    print(f"[*] Sayfa {page_num + 1} goruntuye donusturuluyor...")
    zoom = 3
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)
    
    # PIL Image'e dönüştür
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    width, height = img.size
    
    # Sayfanın üst %10'unu al
    crop_box = (0, 0, width, int(height * 0.1))
    cropped_img = img.crop(crop_box)
    
    print(f"    Goruntu boyutu: {width}x{height}")
    print(f"    Kirpilmis bolge: {cropped_img.size[0]}x{cropped_img.size[1]} (ust %10)")
    
    # Görüntüyü kaydet
    output_img = "test_vision_ocr.png"
    cropped_img.save(output_img)
    print(f"[*] Test edilen bolge kaydedildi: {output_img}")
    
    # OCR için Vision API'ye gönder
    print("\n[*] Google Cloud Vision OCR islemi yapiliyor...")
    
    img_byte_arr = io.BytesIO()
    cropped_img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    
    image = vision.Image(content=img_byte_arr)
    response = vision_client.document_text_detection(
        image=image,
        image_context={"language_hints": ["ar"]}
    )
    
    if response.error.message:
        print(f"[HATA] Vision API hatasi: {response.error.message}")
        return
    
    # OCR sonucu
    arabic_text = response.full_text_annotation.text.strip() if response.full_text_annotation.text else ""
    
    print("\n" + "=" * 80)
    print("SONUCLAR:")
    print("=" * 80)
    
    if not arabic_text:
        print("\n[UYARI] OCR hic metin bulamadi!")
        print(f"Lutfen {output_img} dosyasini kontrol edin.")
        return
    
    print(f"\nARAPCA METIN ({len(arabic_text)} karakter):")
    print("-" * 80)
    print(arabic_text)
    
    # İstatistikler
    kelime_sayisi = len(arabic_text.split())
    satir_sayisi = len(arabic_text.split('\n'))
    
    print("\nISTATISTIKLER:")
    print(f"   Karakter: {len(arabic_text)}")
    print(f"   Kelime: {kelime_sayisi}")
    print(f"   Satir: {satir_sayisi}")
    
    # Sonuçları dosyaya kaydet
    output_txt = "test_vision_ocr_sonuc.txt"
    with open(output_txt, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("3. SAYFA ILK SATIR - GOOGLE VISION OCR SONUCU\n")
        f.write("(Ceviri YOK - Aylik 1000 OCR ucretsiz)\n")
        f.write("=" * 80 + "\n\n")
        f.write("ARAPCA METIN:\n")
        f.write("-" * 80 + "\n")
        f.write(arabic_text + "\n")
    
    print(f"\n[OK] Sonuclar kaydedildi: {output_txt}")
    print(f"[OK] Goruntu kaydedildi: {output_img}")
    print("\n" + "=" * 80)
    print("Test tamamlandi!")
    print("=" * 80)
    
    pdf_document.close()

if __name__ == "__main__":
    try:
        test_vision_only()
    except Exception as e:
        print(f"\n[HATA] {e}")
        import traceback
        traceback.print_exc()
