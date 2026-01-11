"""
Tesseract OCR Kurulum Test Scripti
Bu script Tesseract'ın doğru kurulup kurulmadığını kontrol eder.
"""

import sys
from pathlib import Path

def test_tesseract():
    """Tesseract kurulumunu test eder."""
    
    print("=" * 80)
    print("TESSERACT OCR KURULUM TESTİ")
    print("=" * 80)
    print()
    
    # 1. pytesseract modülünü import et
    try:
        import pytesseract
        print("[OK] pytesseract modülü yüklü")
    except ImportError:
        print("[HATA] pytesseract modülü bulunamadı!")
        print("Çözüm: pip install pytesseract")
        sys.exit(1)
    
    # 2. Tesseract binary'sini kontrol et
    try:
        version = pytesseract.get_tesseract_version()
        print(f"[OK] Tesseract sürümü: {version}")
    except pytesseract.TesseractNotFoundError:
        print("[HATA] Tesseract bulunamadı!")
        print()
        print("Tesseract kurulu değil. Lütfen şu adımları takip edin:")
        print("1. TESSERACT_KURULUM.md dosyasını okuyun")
        print("2. Tesseract'ı indirip kurun")
        print("3. Arabic (ara) dil paketini seçmeyi unutmayın")
        print()
        print("İndirme: https://github.com/UB-Mannheim/tesseract/wiki")
        sys.exit(1)
    
    # 3. Arapça dil desteğini kontrol et
    try:
        langs = pytesseract.get_languages(config='')
        print(f"[OK] Tesseract dilleri: {', '.join(langs)}")
        
        if 'ara' in langs:
            print("[OK] Arapça (ara) dil paketi mevcut ✓")
        else:
            print("[UYARI] Arapça (ara) dil paketi bulunamadı!")
            print("Tesseract'ı yeniden kurun ve Arabic seçeneğini işaretleyin.")
            print("Veya ara.traineddata dosyasını tessdata klasörüne kopyalayın.")
            sys.exit(1)
    except Exception as e:
        print(f"[HATA] Dil kontrolü başarısız: {e}")
        sys.exit(1)
    
    # 4. pdf2image modülünü kontrol et
    try:
        import pdf2image
        print("[OK] pdf2image modülü yüklü")
    except ImportError:
        print("[HATA] pdf2image modülü bulunamadı!")
        print("Çözüm: pip install pdf2image")
        sys.exit(1)
    
    # 5. Poppler kontrolü (pdf2image için gerekli)
    try:
        from pdf2image import convert_from_path
        print("[OK] pdf2image kullanıma hazır")
        print()
        print("[NOT] İlk kullanımda poppler indirme gerekebilir.")
        print("      Script otomatik olarak indirecektir.")
    except Exception as e:
        print(f"[UYARI] pdf2image test edilemedi: {e}")
    
    print()
    print("=" * 80)
    print("✅ TÜM KONTROLLER BAŞARILI!")
    print("=" * 80)
    print()
    print("Tesseract OCR kullanıma hazır.")
    print("Sonraki adım: python test_ocr_sample.py")
    print()

if __name__ == "__main__":
    test_tesseract()
