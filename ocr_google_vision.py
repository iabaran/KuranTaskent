#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Cloud Vision API ile Tek Sayfa OCR
Taskent Mushafi'ndan bir sayfayi okur ve Arapca metni cikartir.
"""

import os
import sys
import json
import argparse
from pathlib import Path
import fitz  # PyMuPDF
from PIL import Image
import io

def extract_page_image(pdf_path, page_number, dpi=300):
    """
    PDF'den belirli bir sayfayi yuksek cozunurluklu goruntu olarak cikartir
    
    Args:
        pdf_path: PDF dosya yolu
        page_number: Sayfa numarasi (1-indexed)
        dpi: Goruntu cozunurlugu (varsayilan: 300)
    
    Returns:
        PIL Image objesi
    """
    pdf_document = fitz.open(pdf_path)
    
    # Sayfa index'i (0-based)
    page_index = page_number - 1
    
    if page_index < 0 or page_index >= len(pdf_document):
        raise ValueError(f"Gecersiz sayfa numarasi: {page_number}. PDF'de {len(pdf_document)} sayfa var.")
    
    page = pdf_document[page_index]
    
    # DPI'ye gore zoom hesapla (72 DPI temel)
    zoom = dpi / 72.0
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)
    
    # PIL Image'e donustur
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    
    pdf_document.close()
    
    return img

def ocr_with_google_vision(image, language_hints=['ar']):
    """
    Google Cloud Vision API ile OCR yapar
    
    Args:
        image: PIL Image objesi
        language_hints: Dil ipuclari (varsayilan: Arapca)
    
    Returns:
        Dict: {
            'text': tam metin,
            'words': kelime listesi,
            'confidence': guven skoru
        }
    """
    from google.cloud import vision
    
    # Vision client olustur
    client = vision.ImageAnnotatorClient()
    
    # PIL Image'i bytes'a cevir
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    
    # Vision API icin Image objesi olustur
    vision_image = vision.Image(content=img_byte_arr)
    
    # Image context (dil ipucu)
    image_context = vision.ImageContext(language_hints=language_hints)
    
    # Document text detection (daha detayli OCR)
    response = client.document_text_detection(
        image=vision_image,
        image_context=image_context
    )
    
    if response.error.message:
        raise Exception(f"Google Vision API hatasi: {response.error.message}")
    
    # Full text
    full_text = response.full_text_annotation.text if response.full_text_annotation else ""
    
    # Kelime bazinda detaylar
    words_data = []
    
    if response.full_text_annotation:
        for page in response.full_text_annotation.pages:
            for block in page.blocks:
                for paragraph in block.paragraphs:
                    for word in paragraph.words:
                        # Kelimeyi olustur
                        word_text = ''.join([symbol.text for symbol in word.symbols])
                        
                        # Bounding box koordinatlari
                        vertices = word.bounding_box.vertices
                        bbox = {
                            'x': vertices[0].x,
                            'y': vertices[0].y,
                            'width': vertices[2].x - vertices[0].x,
                            'height': vertices[2].y - vertices[0].y
                        }
                        
                        # Guven skoru
                        confidence = word.confidence if hasattr(word, 'confidence') else 0.0
                        
                        words_data.append({
                            'text': word_text,
                            'confidence': confidence,
                            'bbox': bbox
                        })
    
    # Ortalama guven skoru
    avg_confidence = sum(w['confidence'] for w in words_data) / len(words_data) if words_data else 0.0
    
    return {
        'text': full_text,
        'words': words_data,
        'confidence': avg_confidence
    }

def main():
    parser = argparse.ArgumentParser(description='Google Vision ile tek sayfa OCR')
    parser.add_argument('--page', type=int, default=3, help='Sayfa numarasi (varsayilan: 3)')
    parser.add_argument('--pdf', type=str, default=None, help='PDF dosya yolu (varsayilan: otomatik bul)')
    parser.add_argument('--output', type=str, default=None, help='Cikti JSON dosyasi (varsayilan: output/page_NNN.json)')
    parser.add_argument('--dpi', type=int, default=300, help='Goruntu cozunurlugu (varsayilan: 300)')
    
    args = parser.parse_args()
    
    print("=" * 80)
    print(f"GOOGLE CLOUD VISION OCR - SAYFA {args.page}")
    print("=" * 80)
    print()
    
    # PDF dosyasini bul
    if args.pdf:
        pdf_path = args.pdf
    else:
        pdf_files = list(Path(".").glob("*Mushaf*.pdf"))
        if not pdf_files:
            print("[HATA] Mushaf PDF dosyasi bulunamadi!")
            sys.exit(1)
        pdf_path = str(pdf_files[0])
    
    print(f"[*] PDF: {pdf_path}")
    print(f"[*] Sayfa: {args.page}")
    print(f"[*] DPI: {args.dpi}")
    print()
    
    # Sayfa goruntusunu cikart
    print("[1/3] Sayfa goruntusu cikariliyor...")
    try:
        image = extract_page_image(pdf_path, args.page, dpi=args.dpi)
        print(f"[OK] Goruntu boyutu: {image.size[0]}x{image.size[1]} piksel")
    except Exception as e:
        print(f"[HATA] Goruntu cikartma basarisiz: {e}")
        sys.exit(1)
    
    # OCR yap
    print()
    print("[2/3] Google Vision OCR yapiliyor...")
    try:
        ocr_result = ocr_with_google_vision(image, language_hints=['ar'])
        print(f"[OK] OCR tamamlandi")
        print(f"[OK] Toplam {len(ocr_result['words'])} kelime tanindi")
        print(f"[OK] Ortalama guven skoru: {ocr_result['confidence']:.2%}")
    except Exception as e:
        print(f"[HATA] OCR basarisiz: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Sonuclari kaydet
    print()
    print("[3/3] Sonuclar kaydediliyor...")
    
    # Output dizini olustur
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Cikti dosya adi
    if args.output:
        output_file = Path(args.output)
    else:
        output_file = output_dir / f"page_{args.page:03d}.json"
    
    # Gorsel de kaydet
    image_file = output_dir / f"page_{args.page:03d}.png"
    image.save(image_file)
    
    # JSON cikti
    output_data = {
        'page_number': args.page,
        'pdf_path': str(pdf_path),
        'image_path': str(image_file),
        'dpi': args.dpi,
        'text': ocr_result['text'],
        'word_count': len(ocr_result['words']),
        'confidence': ocr_result['confidence'],
        'words': ocr_result['words']
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] JSON: {output_file}")
    print(f"[OK] Goruntu: {image_file}")
    
    # Metin onizleme
    print()
    print("=" * 80)
    print("METIN ONIZLEME (ilk 200 karakter):")
    print("=" * 80)
    preview = ocr_result['text'][:200]
    
    # Dosyaya yaz (konsol kodlama sorunu icin)
    preview_file = output_dir / f"page_{args.page:03d}_preview.txt"
    with open(preview_file, 'w', encoding='utf-8') as f:
        f.write(ocr_result['text'])
    
    print(f"[*] Tam metin: {preview_file}")
    print()
    
    print("=" * 80)
    print("[BASARILI] OCR tamamlandi!")
    print("=" * 80)
    print()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
