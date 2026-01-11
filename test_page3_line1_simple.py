#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
3. Sayfa İlk Satır OCR + Çeviri Testi (REST API ile)
"""

import fitz  # PyMuPDF
from PIL import Image
import io
import base64
import requests
from dotenv import load_dotenv
import os
from pathlib import Path

def test_first_line():
    """3. sayfanın ilk satırını OCR + çeviri yapar (REST API kullanarak)"""
    
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
    print("3. SAYFA İLK SATIR TESTİ (Google Cloud Vision REST API)")
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
    
    # Sayfanın üst %10'luk kısmını al (sadece ilk satır için)
    crop_box = (0, 0, width, int(height * 0.1))
    cropped_img = img.crop(crop_box)
    
    print(f"    Görüntü boyutu: {width}x{height}")
    print(f"    Kırpılmış bölge: {cropped_img.size[0]}x{cropped_img.size[1]} (üst %10)")
    
    # Görüntüyü kaydet
    output_img = "test_3_sayfa_ilk_satir.png"
    cropped_img.save(output_img)
    print(f"[*] Test edilen bölge kaydedildi: {output_img}")
    
    # Görüntüyü base64'e çevir
    print("\n[*] Google Cloud Vision OCR işlemi yapılıyor...")
    img_byte_arr = io.BytesIO()
    cropped_img.save(img_byte_arr, format='PNG')
    img_base64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
    
    # Vision API'ye REST isteği gönder
    vision_url = f"https://vision.googleapis.com/v1/images:annotate?key={api_key}"
    
    vision_request = {
        "requests": [
            {
                "image": {
                    "content": img_base64
                },
                "features": [
                    {
                        "type": "DOCUMENT_TEXT_DETECTION"
                    }
                ],
                "imageContext": {
                    "languageHints": ["ar"]
                }
            }
        ]
    }
    
    try:
        response = requests.post(vision_url, json=vision_request)
        response.raise_for_status()
        result = response.json()
        
        if "responses" in result and len(result["responses"]) > 0:
            text_annotations = result["responses"][0].get("fullTextAnnotation", {})
            arabic_text = text_annotations.get("text", "").strip()
        else:
            arabic_text = ""
            
    except Exception as e:
        print(f"[HATA] Vision API hatası: {e}")
        return
    
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
    
    # Türkçe çeviri (Google Translate REST API)
    print(f"\n[*] Türkçe çevirisi yapılıyor...")
    translate_url = f"https://translation.googleapis.com/language/translate/v2?key={api_key}"
    
    translate_request = {
        "q": arabic_text,
        "source": "ar",
        "target": "tr",
        "format": "text"
    }
    
    try:
        response = requests.post(translate_url, json=translate_request)
        response.raise_for_status()
        result = response.json()
        
        if "data" in result and "translations" in result["data"]:
            turkish_text = result["data"]["translations"][0]["translatedText"]
        else:
            turkish_text = "[Çeviri yapılamadı]"
            
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
