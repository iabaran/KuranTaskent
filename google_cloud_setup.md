# Google Cloud Vision API Kurulum Rehberi

## 📋 Genel Bakış

Google Cloud Vision API, el yazması Arapça metinleri tanımak için en iyi OCR çözümüdür. Bu rehber size:
- Google Cloud hesabı açmayı
- Vision API'yi aktif etmeyi
- Credentials oluşturmayı
- Python üzerinden API kullanmayı öğretecek

## 💰 Maliyet Bilgisi

- ✅ **İlk 1,000 sayfa/ay**: TAMAMEN ÜCRETSİZ
- Taşkent Mushafı (1,311 sayfa) ilk ayda ücretsiz işlenebilir
- Kredi kartı bilgisi gerekli ancak onay vermeden ücret kesilmez

---

## 🚀 Adım Adım Kurulum

### Adım 1: Google Cloud Hesabı Oluşturma

1. **Google Cloud Console'a gidin:**
   - URL: https://console.cloud.google.com
   - Google hesabınızla giriş yapın (yoksa oluşturun)

2. **Yeni Proje Oluşturun:**
   - Sol üst köşeden "Select a project" → "NEW PROJECT"
   - Proje adı: `taskent-mushafi-ocr`
   - Create'e tıklayın

### Adım 2: Vision API'yi Aktif Etme

1. **API Library'ye gidin:**
   - Sol menüden: APIs & Services → Library
   - Arama kutusuna "Cloud Vision API" yazın

2. **Vision API'yi Enable edin:**
   - "Cloud Vision API"ye tıklayın
   - "ENABLE" butonuna basın

3. **Translate API'yi de Enable edin (opsiyonel):**
   - Arama kutusuna "Cloud Translation API" yazın
   - Enable edin (Türkçe çeviri için gerekli)

### Adım 3: Service Account Oluşturma

1. **IAM & Admin → Service Accounts:**
   - Sol menüden: IAM & Admin → Service Accounts
   - "CREATE SERVICE ACCOUNT" tıklayın

2. **Service Account Detayları:**
   - Service account name: `taskent-ocr-service`
   - Service account ID: otomatik oluşur
   - Description: "OCR and translation service account"
   - CREATE AND CONTINUE

3. **Rol Atama:**
   - Select a role → "Cloud Vision API User"
   - Add Another Role → "Cloud Translation API User" (opsiyonel)
   - CONTINUE

4. **Key Oluşturma:**
   - DONE'a tıklayın
   - Oluşan service account'un yanındaki ⋮ (3 nokta) → Manage keys
   - ADD KEY → Create new key
   - Key type: JSON
   - CREATE

5. **JSON Key Dosyasını Kaydedin:**
   - İndirilen JSON dosyasını projenize kopyalayın
   - Örnek: `d:\KuranTaskent\google-credentials.json`

### Adım 4: Python Kütüphanelerini Kurma

```bash
pip install google-cloud-vision google-cloud-translate
```

### Adım 5: Environment Variable Ayarlama

#### Windows (PowerShell):
```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS="d:\KuranTaskent\google-credentials.json"
```

#### Windows (Kalıcı):
1. Sistem → Gelişmiş sistem ayarları → Environment Variables
2. Yeni sistem değişkeni ekle:
   - Variable name: `GOOGLE_APPLICATION_CREDENTIALS`
   - Variable value: `d:\KuranTaskent\google-credentials.json`

---

## ✅ Test: Bağlantıyı Doğrulama

Kurulumun başarılı olduğunu test edin:

```bash
python test_google_vision_connection.py
```

Beklenen çıktı:
```
[OK] Google Cloud Vision API baglantisi basarili!
[OK] Service account: taskent-ocr-service@...
```

---

## 🔒 Güvenlik Uyarıları

> [!CAUTION]
> **Credentials dosyasını asla git'e commit etmeyin!**

`.gitignore` dosyanıza ekleyin:
```
google-credentials.json
*.json  # tüm credential dosyaları
.env
```

---

## 🆘 Sorun Giderme

### Hata: "Permission denied"
- Service account'a doğru roller atandığından emin olun
- Vision API'nin Enable olduğunu kontrol edin

### Hata: "Quota exceeded"
- API kullanımınızı kontrol edin: Console → APIs & Services → Dashboard
- Aylık 1,000 sayfa limitini aştıysanız faturalandırma aktif olmalı

### Hata: "Could not find credentials"
- `GOOGLE_APPLICATION_CREDENTIALS` environment variable doğru mu?
- JSON dosyası doğru konumda mı?

---

## 📚 Ek Kaynaklar

- [Google Vision API Documentation](https://cloud.google.com/vision/docs)
- [Python Client Library](https://googleapis.dev/python/vision/latest/)
- [Pricing Calculator](https://cloud.google.com/products/calculator)
