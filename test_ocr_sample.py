"""
OCR Kalite Test Scripti (Alternatif Yaklaşım)
pdfplumber kullanarak görüntüleri çıkarır ve OCR uygular.
"""

import pdfplumber
import pytesseract
from pathlib import Path
import sys
from datetime import datetime
from PIL import Image
import io

def test_ocr_on_sample_pages(pdf_path, num_pages=5, output_path="ocr_test_sample.txt"):
    """
    PDF'in ilk birkaç sayfasında OCR testi yapar.
    
    Args:
        pdf_path: PDF dosyasının yolu
        num_pages: Test edilecek sayfa sayısı (varsayılan: 5)
        output_path: Çıktı dosyası
    """
    print(f"PDF: {pdf_path.name}")
    print(f"Test edilecek sayfa sayısı: {num_pages}")
    print("=" * 80)
    print()
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            pages_to_process = min(num_pages, total_pages)
            
            print(f"Toplam sayfa: {total_pages}")
            print(f"İşlenecek: {pages_to_process}")
            print()
            
            with open(output_path, 'w', encoding='utf-8') as output_file:
                for i in range(pages_to_process):
                    page_num = i + 1
                    page = pdf.pages[i]
                    
                    print(f"Sayfa {page_num}/{pages_to_process} işleniyor...", end=" ")
                    
                    try:
                        # Sayfayı görüntüye dönüştür
                        img = page.to_image(resolution=300)
                        pil_image = img.original
                        
                        # OCR uygula
                        text = pytesseract.image_to_string(
                            pil_image,
                            lang='ara',
                            config='--psm 6'
                        )
                        
                        # Dosyaya yaz
                        output_file.write(f"\n{'='*80}\n")
                        output_file.write(f"SAYFA {page_num}\n")
                        output_file.write(f"{'='*80}\n\n")
                        output_file.write(text)
                        output_file.write("\n\n")
                        
                        # İstatistik
                        char_count = len(text.strip())
                        word_count = len(text.split())
                        print(f"✓ ({char_count} karakter, {word_count} kelime)")
                        
                    except Exception as e:
                        error_msg = f"HATA: {str(e)}"
                        print(error_msg)
                        output_file.write(f"\n{error_msg}\n")
        
        print()
        print("=" * 80)
        print("[OK] OCR testi tamamlandi!")
        print(f"[OK] Cikti dosyasi: {output_path}")
        
        # Dosya boyutu
        file_size = Path(output_path).stat().st_size
        print(f"[OK] Dosya boyutu: {file_size:,} bytes ({file_size/1024:.2f} KB)")
        print()
        
        # Kalite değerlendirmesi
        print("=" * 80)
        print("KALITE DEGERLENDIRMESI")
        print("=" * 80)
        print()
        print("Lutfen cikti dosyasini acarak OCR kalitesini kontrol edin:")
        print(f"  {output_path}")
        print()
        print("Kontrol listesi:")
        print("  - Arapca harfler duzgun taninmis mi?")
        print("  - Kelimeler okunabilir durumda mi?")
        print("  - Satir duzeni korunmus mu?")
        print()
        print("Eger kalite kabul edilebilirse:")
        print("  python extract_text_ocr.py")
        print()
        print("Eger kalite kotuyse:")
        print("  - DPI degerini artirmayi deneyin (resolution=400 veya 600)")
        print("  - Veya cloud OCR servisine gecmeyi dusunun")
        print()
        
    except Exception as e:
        print(f"HATA: OCR test islemi basarisiz: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def main():
    # PDF dosyasını bul
    pdf_files = list(Path(".").glob("*.pdf"))
    
    if not pdf_files:
        print("HATA: Bu dizinde PDF dosyasi bulunamadi!")
        sys.exit(1)
    
    pdf_path = pdf_files[0]
    
    print()
    print("TASKENT MUSHAFI OCR KALITE TESTI")
    print("=" * 80)
    print()
    
    start_time = datetime.now()
    print(f"Baslangic: {start_time.strftime('%H:%M:%S')}")
    print()
    
    # İlk 5 sayfayı test et
    test_ocr_on_sample_pages(pdf_path, num_pages=5)
    
    end_time = datetime.now()
    duration = end_time - start_time
    print(f"Bitis: {end_time.strftime('%H:%M:%S')}")
    print(f"Sure: {duration}")
    print()

if __name__ == "__main__":
    main()
