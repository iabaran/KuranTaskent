# Tesseract OCR Kurulum Rehberi

## 📥 Tesseract OCR Kurulumu (Windows)

### Adım 1: Tesseract'ı İndirin ve Kurun

1. **İndirme Linki**: https://github.com/UB-Mannheim/tesseract/wiki
   - En son sürümü indirin (örn: `tesseract-ocr-w64-setup-5.x.x.exe`)

2. **Kurulum Sırasında ÖNEMLİ:**
   - Kurulum sırasında **"Additional language data"** bölümünde:
   - ✅ **Arabic** (ara) seçeneğini işaretleyin
   - Bu Arapça metin tanıma için gereklidir

3. **Kurulum Yolu:**
   - Varsayılan: `C:\Program Files\Tesseract-OCR`
   - Bu yolu not edin (scriptte kullanacağız)

### Adım 2: Kurulumu Doğrulayın

Kurulumdan sonra yeni bir PowerShell penceresi açın ve şunu çalıştırın:

```powershell
tesseract --version
```

**Beklenen çıktı:**
```
tesseract v5.x.x
...
```

Eğer hata alırsanız:
- Bilgisayarınızı yeniden başlatın
- Veya PATH'i manuel olarak ekleyin (Adım 3)

### Adım 3: PATH Ayarı (Gerekirse)

Eğer `tesseract --version` çalışmazsa:

1. **Windows Arama** → "Environment Variables" / "Ortam Değişkenleri"
2. **System Properties** → **Environment Variables**
3. **System variables** altında **Path** seçin, **Edit** tıklayın
4. **New** tıklayın ve ekleyin: `C:\Program Files\Tesseract-OCR`
5. **OK** ile kaydedin
6. PowerShell'i kapatıp yeniden açın

### Adım 4: Arapça Dil Dosyasını Kontrol Edin

Kurulum dizininde `tessdata` klasörünü kontrol edin:
```
C:\Program Files\Tesseract-OCR\tessdata\ara.traineddata
```

Bu dosya **mutlaka** mevcut olmalıdır. Yoksa:
- Buradan indirin: https://github.com/tesseract-ocr/tessdata
- `ara.traineddata` dosyasını `tessdata` klasörüne kopyalayın

## ✅ Kurulum Tamamlandı mı?

Kurulumu tamamladıktan sonra, proje dizininde şu komutu çalıştırın:
```powershell
python test_tesseract.py
```

Bu script Tesseract'ın düzgün çalışıp çalışmadığını test edecek.

## 🚀 Sonraki Adımlar

Tesseract başarıyla kurulduktan sonra:
1. `python test_ocr_sample.py` - İlk 5 sayfayı test et
2. Sonuçları incele
3. Kalite kabul edilebilirse tüm PDF'i işle
