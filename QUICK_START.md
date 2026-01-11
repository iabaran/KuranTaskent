# 🚀 Hızlı Başlangıç Rehberi

## Mevcut Durum

✅ **Hazır olan dosyalar:**
- [`google_cloud_setup.md`](file:///d:/KuranTaskent/google_cloud_setup.md) - Detaylı kurulum rehberi
- [`test_google_vision_connection.py`](file:///d:/KuranTaskent/test_google_vision_connection.py) - Bağlantı testi
- [`ocr_google_vision.py`](file:///d:/KuranTaskent/ocr_google_vision.py) - OCR scripti
- [`requirements.txt`](file:///d:/KuranTaskent/requirements.txt) - Güncellenmiş bağımlılıklar
- [`.env.example`](file:///d:/KuranTaskent/.env.example) - Environment variable template

---

## 📋 Adım Adım Kullanım

### 1️⃣ **Google Cloud Kurulumu** (İlk Kez Yapılacak)

#### a) Google Cloud Hesabı Oluşturun
1. https://console.cloud.google.com adresine gidin
2. Google hesabınızla giriş yapın
3. Yeni proje oluşturun: `taskent-mushafi-ocr`

#### b) Vision API'yi Aktif Edin
1. APIs & Services → Library
2. "Cloud Vision API" arayın ve Enable edin

#### c) Service Account Oluşturun
1. IAM & Admin → Service Accounts → CREATE SERVICE ACCOUNT
2. Name: `taskent-ocr-service`
3. Role: `Cloud Vision API User`
4. JSON key indirin → `google-credentials.json` olarak projeye kaydedin

📖 **Detaylı rehber:** [`google_cloud_setup.md`](file:///d:/KuranTaskent/google_cloud_setup.md)

---

### 2️⃣ **Kütüphaneleri Kurun**

```powershell
pip install google-cloud-vision google-cloud-translate
```

---

### 3️⃣ **Environment Variable Ayarlayın**

#### PowerShell (geçici):
```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS="d:\KuranTaskent\google-credentials.json"
```

#### Windows (kalıcı):
1. Sistem → Gelişmiş sistem ayarları → Environment Variables
2. Yeni değişken:
   - Name: `GOOGLE_APPLICATION_CREDENTIALS`
   - Value: `d:\KuranTaskent\google-credentials.json`

---

### 4️⃣ **Bağlantı Testi**

```powershell
python test_google_vision_connection.py
```

**Beklenen çıktı:**
```
[OK] Google Cloud Vision API baglantisi basarili!
[OK] Service Account: taskent-ocr-service@...
```

---

### 5️⃣ **İlk OCR Testi** ⭐

Sayfa 3'ü test edin:

```powershell
python ocr_google_vision.py --page 3
```

**Sonuçlar:**
- `output/page_003.json` - Tam OCR verisi (kelimeler + koordinatlar)
- `output/page_003.png` - Sayfa görüntüsü
- `output/page_003_preview.txt` - Arapça metin (UTF-8)

---

### 6️⃣ **Sonuçları İnceleyin**

#### JSON Dosyasını Açın:
```powershell
notepad output\page_003.json
```

**İçerik örneği:**
```json
{
  "page_number": 3,
  "text": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ...",
  "word_count": 156,
  "confidence": 0.98,
  "words": [
    {
      "text": "بِسْمِ",
      "confidence": 0.99,
      "bbox": {"x": 100, "y": 50, "width": 45, "height": 30}
    }
  ]
}
```

#### Metin Dosyasını Açın:
```powershell
notepad output\page_003_preview.txt
```

---

## ✅ Başarı Kriterleri

Google Cloud Vision ile OCR başarılıysa:

- ✅ `confidence` > 0.90 (>%90 güvenle doğru)
- ✅ Arapça harfler düzgün tanınıyor
- ✅ Kelimeler anlamlı

**Tesseract ile karşılaştırma:**
- ❌ Tesseract: Anlamsız karakterler
- ✅ Google Vision: Düzgün Arapça metin

---

## 🎯 Sonraki Adımlar

### Eğer OCR Kalitesi İyiyse:

#### 1. Batch Processing (Tüm PDF)
Tüm sayfaları işleyen script hazır değil, şimdi onu oluşturacağız.

#### 2. Türkçe Çeviri Ekle
Her kelime için Türkçe anlam ekleyeceğiz (Google Translate veya offline sözlük).

#### 3. Manuel Düzenleme Arayüzü
İsteğe bağlı: Web tabanlı düzenleme arayüzü.

---

## ⚠️ Sorun Giderme

### "Permission denied"
→ Service account'a `Cloud Vision API User` rolü atandı mı?

### "Quota exceeded"
→ Google Cloud Console → APIs & Services → Dashboard'dan kullanımı kontrol edin

### "Could not find credentials"
→ Environment variable doğru ayarlandı mı?
```powershell
echo $env:GOOGLE_APPLICATION_CREDENTIALS
```

---

## 💰 Maliyet Hatırlatma

- İlk 1,000 sayfa/ay: **ÜCRETSİZ** ✅
- Taşkent Mushafı (1,311 sayfa) → İlk 1,000 sayfa ücretsiz
- Kalan 311 sayfa → ~$0.47 (çok düşük)

**Toplam maliyet:** ~$0.50 (sadece OCR için)

---

## 📞 Yardım

Herhangi bir sorun olursa:
1. [`google_cloud_setup.md`](file:///d:/KuranTaskent/google_cloud_setup.md) dosyasındaki "Sorun Giderme" bölümüne bakın
2. Bana bildirin!
