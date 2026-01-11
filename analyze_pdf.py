"""
PDF Analiz Scripti
Bu script, PDF dosyasının yapısını analiz eder ve OCR gereksinimini belirler.
"""

import pdfplumber
from pathlib import Path
import sys

def analyze_pdf(pdf_path):
    """
    PDF dosyasının içeriğini analiz eder.
    
    Args:
        pdf_path: PDF dosyasının yolu
    """
    print(f"PDF dosyası analiz ediliyor: {pdf_path.name}")
    print("=" * 80)
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            print(f"Toplam sayfa sayısı: {total_pages}\n")
            
            # İlk 10 sayfayı detaylı analiz et
            pages_to_check = min(10, total_pages)
            print(f"İlk {pages_to_check} sayfa detaylı analiz ediliyor...\n")
            
            text_found_count = 0
            image_found_count = 0
            
            for i in range(pages_to_check):
                page = pdf.pages[i]
                page_num = i + 1
                
                # Metin kontrolü
                text = page.extract_text()
                has_text = text and len(text.strip()) > 0
                
                # Görüntü kontrolü
                images = page.images
                has_images = len(images) > 0
                
                if has_text:
                    text_found_count += 1
                if has_images:
                    image_found_count += 1
                
                # Sayfa bilgileri
                print(f"Sayfa {page_num}:")
                print(f"  - Boyut: {page.width:.2f} x {page.height:.2f}")
                print(f"  - Metin var mı: {'EVET' if has_text else 'HAYIR'}")
                print(f"  - Görüntü sayısı: {len(images)}")
                
                if has_text:
                    text_preview = text.strip()[:100].replace('\n', ' ')
                    print(f"  - Metin önizleme: {text_preview}...")
                
                print()
            
            # Analiz sonucu
            print("=" * 80)
            print("ANALİZ SONUCU:")
            print("=" * 80)
            print(f"İncelenen sayfa sayısı: {pages_to_check}")
            print(f"Metin içeren sayfa: {text_found_count}")
            print(f"Görüntü içeren sayfa: {image_found_count}")
            
            if text_found_count == 0:
                print("\n[!] PDF'de hiç metin bulunamadı!")
                print("[!] Bu PDF taranmış görüntülerden oluşuyor.")
                print("[!] Metin çıkarmak için OCR (Optical Character Recognition) gerekli.")
                print("\nÖnerilen çözümler:")
                print("1. Tesseract OCR kullanarak metin çıkarma")
                print("2. Google Cloud Vision API, Azure Computer Vision gibi cloud OCR servisleri")
                print("3. Adobe Acrobat gibi profesyonel OCR araçları")
            elif text_found_count < pages_to_check:
                print("\n[!] Bazı sayfalarda metin yok.")
                print("[!] Karma (hibrit) PDF - hem metin hem görüntü içeriyor.")
            else:
                print("\n[OK] Tüm sayfalar metin içeriyor.")
                print("[OK] OCR gerekmeyebilir, ancak çıkarılan metin boşsa görüntü tabanlıdır.")
            
            # İlk sayfanın görüntüsünü kaydet (varsa)
            if total_pages > 0:
                first_page = pdf.pages[0]
                if first_page.images:
                    print("\n[İPUCU] İlk sayfa görüntü içeriyor.")
                    print("[İPUCU] PDF'in nasıl göründüğünü görmek için PDF okuyucu kullanın.")
            
    except Exception as e:
        print(f"HATA: PDF analiz edilirken bir hata oluştu: {str(e)}")
        sys.exit(1)

def main():
    # PDF dosyasını bul
    pdf_files = list(Path(".").glob("*.pdf"))
    
    if not pdf_files:
        print("HATA: Bu dizinde PDF dosyası bulunamadı!")
        sys.exit(1)
    
    pdf_path = pdf_files[0]
    analyze_pdf(pdf_path)

if __name__ == "__main__":
    main()
