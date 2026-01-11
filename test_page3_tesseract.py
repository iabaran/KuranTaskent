#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
3. Sayfa İlk Satır - Tesseract OCR Testi (Tamamen Ücretsiz)
"""

import fitz  # PyMuPDF
from PIL import Image
import pytesseract
from pathlib import Path

def test_first_line_tesseract():
    """3. sayfanın ilk satırını Tesseract ile OCR yapar"""
    
    # PDF dosyasını bul
    pdf_files = list(Path(".").glob("*Mushaf*.pdf"))
    
    if not pdf_files:
        print("[HATA] Mushaf PDF dosyası bulunamadı!")
        return
    
    pdf_path = str(pdf_files[0])
    
    print("=" * 80)
    print("3. SAYFA İLK SATIR TESTİ (Tesseract OCR - Ücretsiz)")
    print("=" * 80)
    print()
    
    # PDF'i aç
    print(f"[*] PDF açılıyor: {pdf_path}")
    pdf_document = fitz.open(pdf_path)
    
    # 3. sayfayı al (index 2)
    page_num = 2
    page = pdf_document[page_num]
    
    # Sayfayı yüksek çözünürlükte görüntüye çevir
    print(f"[*] Sayfa {page_num + 1} görüntüye dönüştürülüyor...")
    zoom = 3  # Yüksek kalite
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)
    
    # PIL Image'e dönüştür
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    width, height = img.size
    
    # Sayfanın üst %15'lik kısmını al (ilk satırlar için)
    crop_box = (0, 0, width, int(height * 0.15))
    cropped_img = img.crop(crop_box)
    
    print(f"    Görüntü boyutu: {width}x{height}")
    print(f"    Kırpılmış bölge: {cropped_img.size[0]}x{cropped_img.size[1]} (üst %15)")
    
    # Görüntüyü kaydet
    output_img = "test_3_sayfa_tesseract.png"
    cropped_img.save(output_img)
    print(f"[*] Test edilen bölge kaydedildi: {output_img}")
    
    # Tesseract OCR
    print("\n[*] Tesseract OCR işlemi yapılıyor (Arapça)...")
    
    # Tesseract ayarları
    custom_config = r'--oem 3 --psm 6'  # LSTM engine, tek metin bloğu
    
    try:
        arabic_text = pytesseract.image_to_string(
            cropped_img, 
            lang='ara',
            config=custom_config
        ).strip()
    except Exception as e:
        print(f"[HATA] Tesseract OCR hatası: {e}")
        return
    
    print("\n" + "=" * 80)
    print("SONUÇLAR:")
    print("=" * 80)
    
    if not arabic_text:
        print("\n[UYARI] OCR hiç metin bulamadı!")
        print(f"Lütfen {output_img} dosyasını kontrol edin.")
        print("\nOlası nedenler:")
        print("- Görüntü kalitesi düşük olabilir")
        print("- El yazısı Tesseract için zor olabilir")
        print("- Arapça dil dosyası (ara) kurulu olmayabilir")
    else:
        print(f"\n📖 ARAPÇA METİN ({len(arabic_text)} karakter):")
        print("-" * 80)
        print(arabic_text)
        
        # İstatistikler
        kelime_sayisi = len(arabic_text.split())
        satir_sayisi = len(arabic_text.split('\n'))
        
        print("\n📊 İSTATİSTİKLER:")
        print(f"   Karakter: {len(arabic_text)}")
        print(f"   Kelime: {kelime_sayisi}")
        print(f"   Satır: {satir_sayisi}")
    
    # Sonuçları dosyaya kaydet
    output_txt = "test_3_sayfa_tesseract_sonuc.txt"
    with open(output_txt, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("3. SAYFA İLK SATIR - TESSERACT OCR SONUCU (ÜCRETSIZ)\n")
        f.write("=" * 80 + "\n\n")
        f.write("ARAPÇA METİN:\n")
        f.write("-" * 80 + "\n")
        f.write(arabic_text if arabic_text else "[Metin bulunamadı]")
        f.write("\n")
    
    print(f"\n[✓] Sonuçlar kaydedildi: {output_txt}")
    print(f"[✓] Görüntü kaydedildi: {output_img}")
    print("\n" + "=" * 80)
    print("✅ Test tamamlandı! (Tamamen ücretsiz)")
    print("=" * 80)
    
    pdf_document.close()
    
    # Notlar
    print("\n💡 NOTLAR:")
    print("   • Bu test Tesseract kullanıyor - tamamen ücretsiz ve offline")
    print("   • El yazısı için kalite düşük olabilir")
    print("   • Google Cloud Vision daha iyi sonuç verir ama ücretli")
    print(f"   • Sonuçları {output_txt} dosyasında inceleyebilirsiniz")

if __name__ == "__main__":
    try:
        test_first_line_tesseract()
    except Exception as e:
        print(f"\n[HATA] {e}")
        import traceback
        traceback.print_exc()
