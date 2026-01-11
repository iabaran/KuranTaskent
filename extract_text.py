"""
Taşkent Mushafı PDF'inden Metin Çıkarma Scripti
Bu script, PDF dosyasından tüm sayfaların metnini çıkarır ve txt dosyasına kaydeder.
"""

import pdfplumber
from pathlib import Path
import sys
from datetime import datetime

def extract_text_from_pdf(pdf_path, output_path):
    """
    PDF dosyasından metin çıkarır ve txt dosyasına kaydeder.
    
    Args:
        pdf_path: PDF dosyasının yolu
        output_path: Çıktı txt dosyasının yolu
    """
    print(f"PDF dosyası açılıyor: {pdf_path}")
    print(f"Çıktı dosyası: {output_path}")
    print("=" * 80)
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            print(f"Toplam sayfa sayısı: {total_pages}")
            print("Metin çıkarma başlıyor...")
            print("=" * 80)
            
            # Çıktı dosyasını aç
            with open(output_path, 'w', encoding='utf-8') as output_file:
                # Her sayfayı işle
                for page_num, page in enumerate(pdf.pages, start=1):
                    try:
                        # Sayfadan metin çıkar
                        text = page.extract_text()
                        
                        if text:
                            # Sayfa başlığı ekle
                            output_file.write(f"\n{'='*80}\n")
                            output_file.write(f"SAYFA {page_num}\n")
                            output_file.write(f"{'='*80}\n\n")
                            output_file.write(text)
                            output_file.write("\n\n")
                        
                        # İlerleme durumunu göster (her 10 sayfada bir)
                        if page_num % 10 == 0 or page_num == total_pages:
                            progress = (page_num / total_pages) * 100
                            print(f"İşleniyor: {page_num}/{total_pages} sayfa ({progress:.1f}%)")
                    
                    except Exception as e:
                        error_msg = f"HATA - Sayfa {page_num}: {str(e)}\n"
                        print(error_msg)
                        output_file.write(f"\n{error_msg}\n")
                        continue
            
            print("=" * 80)
            print(f"[OK] Metin çıkarma tamamlandı!")
            print(f"[OK] Çıktı dosyası: {output_path}")
            
            # Dosya boyutu bilgisi
            file_size = Path(output_path).stat().st_size
            print(f"[OK] Çıktı dosya boyutu: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)")

            
    except Exception as e:
        print(f"HATA: PDF işlenirken bir hata oluştu: {str(e)}")
        sys.exit(1)

def main():
    # PDF dosyasını glob ile bul
    pdf_files = list(Path(".").glob("*.pdf"))
    
    if not pdf_files:
        print("HATA: Bu dizinde PDF dosyası bulunamadı!")
        sys.exit(1)
    
    if len(pdf_files) > 1:
        print("Birden fazla PDF dosyası bulundu:")
        for i, pdf in enumerate(pdf_files, 1):
            print(f"{i}. {pdf.name}")
        print("İlk PDF dosyası işlenecek...")
    
    pdf_path = pdf_files[0]
    output_path = Path("extracted_text.txt")
    
    print(f"İşlenecek PDF: {pdf_path.name}")
    
    # Başlangıç zamanı
    start_time = datetime.now()
    print(f"\nBaşlangıç zamanı: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Metin çıkarma
    extract_text_from_pdf(pdf_path, output_path)
    
    # Bitiş zamanı
    end_time = datetime.now()
    duration = end_time - start_time
    print(f"\nBitiş zamanı: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Toplam süre: {duration}")


if __name__ == "__main__":
    main()
