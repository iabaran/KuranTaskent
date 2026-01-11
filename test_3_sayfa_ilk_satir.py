#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
3. Sayfa İlk Satır OCR + Çeviri Testi
"""

import fitz  # PyMuPDF
from google.cloud import vision
from google.cloud import translate_v2 as translate
from PIL import Image
import io
import os
from pathlib import Path
from dotenv import load_dotenv

def test_first_line():
    """3. sayfanın ilk satırını OCR + çeviri yapar"""
    
    # .env dosyasını yükle
    load_dotenv()
    
    # API Key'i al
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("[HATA] .env dosyasında GOOGLE_API_KEY bulunamadı!")
        return
    
    # PDF dosyasını bul
    pdf_files = list(Path(".").glob("*Mushaf*.pdf"))
    
    if not pdf_files:
        print("[HATA] Mushaf PDF dosyası bulunamadı!")
        return
    
    pdf_path = str(pdf_files[0])
    
    print("=" * 80)
    print("3. SAYFA İLK SATIR TESTİ (Google Cloud Vision + Çeviri)")
    print("=" * 80)
    print()
    
    # Google Cloud istemcilerini oluştur (API Key ile)
    try:
        # API Key kullanarak client oluştur
        os.environ['GOOGLE_API_KEY'] = api_key
        vision_client = vision.ImageAnnotatorClient()
        translate_client = translate.Client()
        print("[✓] Google Cloud bağlantısı başarılı")
    except Exception as e:
        print(f"[HATA] Google Cloud bağlantısı kurulamadı: {e}")
        print("\nŞunları kontrol edin:")
        print("1. .env dosyasında GOOGLE_API_KEY ayarlı mı?")
        print("2. API Key geçerli mi?")
        return
    
    # PDF'i aç
    print(f"\n[*] PDF açılıyor: {pdf_path}")
    pdf_document = fitz.open(pdf_path)
    
    # 3. sayfayı al (index 2)
    page_num = 2
    page = pdf_document[page_num]
    
    # Sayfayı yüksek çözünürlükte görüntüye çevir
    print(f"[*] Sayfa {page_num + 1} görüntüye dönüştürülüyor...")
    zoom = 3  # Google Vision için yüksek kalite
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)
    
    # PIL Image'e dönüştür
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    width, height = img.size
    
    # Sayfanın üst %10'luk kısmını al (sadece ilk satır için)
    crop_box = (0, 0, width, int(height * 0.1))
    cropped_img = img.crop(crop_box)
    
    print(f"    Görüntü boyutu: {width}x{height}")
    print(f"    Kırpılmış bölge: {cropped_img.size[0]}x{cropped_img.size[1]} (üst %10)")
    
    # Görüntüyü kaydet
    output_img = "test_3_sayfa_ilk_satir.png"
    cropped_img.save(output_img)
    print(f"[*] Test edilen bölge kaydedildi: {output_img}")
    
    # OCR için Google Vision'a gönder
    print("\n[*] Google Cloud Vision OCR işlemi yapılıyor...")
    
    # Görüntüyü byte array'e çevir
    img_byte_arr = io.BytesIO()
    cropped_img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    
    # Vision API'ye gönder
    image = vision.Image(content=img_byte_arr)
    response = vision_client.document_text_detection(
        image=image,
        image_context={"language_hints": ["ar"]}
    )
    
    if response.error.message:
        print(f"[HATA] Google Vision hatası: {response.error.message}")
        return
    
    # OCR sonucu
    arabic_text = response.full_text_annotation.text.strip() if response.full_text_annotation.text else ""
    
    print("\n" + "=" * 80)
    print("SONUÇLAR:")
    print("=" * 80)
    
    if not arabic_text:
        print("\n[UYARI] OCR hiç metin bulamadı!")
        print(f"Lütfen {output_img} dosyasını kontrol edin.")
        return
    
    print(f"\n📖 ARAPÇA METİN ({len(arabic_text)} karakter):")
    print("-" * 80)
    print(arabic_text)
    
    # Türkçe çeviri
    print(f"\n[*] Türkçe çevirisi yapılıyor...")
    try:
        translation = translate_client.translate(
            arabic_text,
            source_language='ar',
            target_language='tr'
        )
        
        turkish_text = translation['translatedText']
        
        print("\n🇹🇷 TÜRKÇE ÇEVİRİ:")
        print("-" * 80)
        print(turkish_text)
        
    except Exception as e:
        print(f"[HATA] Çeviri yapılamadı: {e}")
        turkish_text = "[Çeviri yapılamadı]"
    
    # Sonuçları dosyaya kaydet
    output_txt = "test_3_sayfa_ilk_satir_sonuc.txt"
    with open(output_txt, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("3. SAYFA İLK SATIR - OCR VE ÇEVİRİ SONUCU\n")
        f.write("=" * 80 + "\n\n")
        f.write("ARAPÇA METİN:\n")
        f.write("-" * 80 + "\n")
        f.write(arabic_text + "\n\n")
        f.write("TÜRKÇE ÇEVİRİ:\n")
        f.write("-" * 80 + "\n")
        f.write(turkish_text + "\n")
    
    print(f"\n[✓] Sonuçlar kaydedildi: {output_txt}")
    print("\n" + "=" * 80)
    print("✅ Test tamamlandı!")
    print("=" * 80)
    
    pdf_document.close()

if __name__ == "__main__":
    try:
        test_first_line()
    except Exception as e:
        print(f"\n[HATA] {e}")
        import traceback
        traceback.print_exc()
