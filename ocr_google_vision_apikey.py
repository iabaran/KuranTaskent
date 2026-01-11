#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Cloud Vision API ile Tek Sayfa OCR (API Key versiyonu)
Service account yerine API Key kullanir.
"""

import os
import sys
import json
import argparse
from pathlib import Path
import fitz  # PyMuPDF
from PIL import Image
import io
import base64
import requests

def extract_page_image(pdf_path, page_number, dpi=300):
    """
    PDF'den belirli bir sayfayi yuksek cozunurluklu goruntu olarak cikartir
    """
    pdf_document = fitz.open(pdf_path)
    page_index = page_number - 1
    
    if page_index < 0 or page_index >= len(pdf_document):
        raise ValueError(f"Gecersiz sayfa numarasi: {page_number}. PDF'de {len(pdf_document)} sayfa var.")
    
    page = pdf_document[page_index]
    zoom = dpi / 72.0
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    pdf_document.close()
    
    return img

def ocr_with_api_key(image, api_key, language_hints=['ar']):
    """
    Google Cloud Vision API ile OCR yapar (API Key kullanarak)
    
    Args:
        image: PIL Image objesi
        api_key: Google Cloud API Key
        language_hints: Dil ipuclari
    
    Returns:
        Dict: OCR sonuclari
    """
    # PIL Image'i base64'e cevir
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    img_base64 = base64.b64encode(img_byte_arr).decode('utf-8')
    
    # API endpoint
    url = f"https://vision.googleapis.com/v1/images:annotate?key={api_key}"
    
    # Request payload
    payload = {
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
                    "languageHints": language_hints
                }
            }
        ]
    }
    
    # API'ye request gonder
    response = requests.post(url, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"API Error: {response.status_code} - {response.text}")
    
    result = response.json()
    
    if 'error' in result:
        raise Exception(f"Vision API Error: {result['error']}")
    
    # Response parse et
    responses = result.get('responses', [])
    if not responses:
        return {'text': '', 'words': [], 'confidence': 0.0}
    
    annotation = responses[0]
    full_text = annotation.get('fullTextAnnotation', {}).get('text', '')
    
    # Kelime bazinda detaylar
    words_data = []
    pages = annotation.get('fullTextAnnotation', {}).get('pages', [])
    
    for page in pages:
        for block in page.get('blocks', []):
            for paragraph in block.get('paragraphs', []):
                for word in paragraph.get('words', []):
                    # Kelime olustur
                    word_text = ''.join([symbol.get('text', '') for symbol in word.get('symbols', [])])
                    
                    # Bounding box
                    vertices = word.get('boundingBox', {}).get('vertices', [])
                    if len(vertices) >= 3:
                        bbox = {
                            'x': vertices[0].get('x', 0),
                            'y': vertices[0].get('y', 0),
                            'width': vertices[2].get('x', 0) - vertices[0].get('x', 0),
                            'height': vertices[2].get('y', 0) - vertices[0].get('y', 0)
                        }
                    else:
                        bbox = {'x': 0, 'y': 0, 'width': 0, 'height': 0}
                    
                    # Guven skoru
                    confidence = word.get('confidence', 0.0)
                    
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
    parser = argparse.ArgumentParser(description='Google Vision ile tek sayfa OCR (API Key)')
    parser.add_argument('--page', type=int, default=3, help='Sayfa numarasi')
    parser.add_argument('--pdf', type=str, default=None, help='PDF dosya yolu')
    parser.add_argument('--output', type=str, default=None, help='Cikti JSON dosyasi')
    parser.add_argument('--dpi', type=int, default=300, help='Goruntu cozunurlugu')
    parser.add_argument('--api-key', type=str, default=None, help='Google Cloud API Key')
    
    args = parser.parse_args()
    
    # API Key kontrol
    api_key = args.api_key or os.environ.get('GOOGLE_VISION_API_KEY')
    if not api_key:
        print("[HATA] API Key bulunamadi!")
        print()
        print("Cozum 1 (Parametre):")
        print("  python ocr_google_vision_apikey.py --api-key YOUR_API_KEY")
        print()
        print("Cozum 2 (Environment Variable):")
        print("  $env:GOOGLE_VISION_API_KEY='YOUR_API_KEY'")
        print("  python ocr_google_vision_apikey.py")
        sys.exit(1)
    
    print("=" * 80)
    print(f"GOOGLE CLOUD VISION OCR (API KEY) - SAYFA {args.page}")
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
        ocr_result = ocr_with_api_key(image, api_key, language_hints=['ar'])
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
    
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    if args.output:
        output_file = Path(args.output)
    else:
        output_file = output_dir / f"page_{args.page:03d}.json"
    
    image_file = output_dir / f"page_{args.page:03d}.png"
    image.save(image_file)
    
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
    preview_file = output_dir / f"page_{args.page:03d}_preview.txt"
    with open(preview_file, 'w', encoding='utf-8') as f:
        f.write(ocr_result['text'])
    
    print(f"[OK] Tam metin: {preview_file}")
    print()
    
    print("=" * 80)
    print("[BASARILI] OCR tamamlandi!")
    print("=" * 80)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
