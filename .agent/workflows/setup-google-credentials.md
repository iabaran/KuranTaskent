---
description: Google Cloud Service Account Oluşturma
---

# Google Cloud Service Account Oluşturma

Vision API'yi kullanmak için service account credentials gerekiyor.

## Adımlar:

1. **Console'a Git**:
   - https://console.cloud.google.com/iam-admin/serviceaccounts?project=taskent-mushafi-ocr

2. **Service Account Oluştur**:
   - "CREATE SERVICE ACCOUNT" butonuna tıkla
   - İsim: `ocr-service-account`
   - Açıklama: `OCR ve çeviri için`
   - "CREATE AND CONTINUE" tıkla

3. **Rol Ver**:
   - Role seçin: `Cloud Vision AI Service Agent`
   - "CONTINUE" tıkla
   - "DONE" tıkla

4. **JSON Key İndir**:
   - Oluşturduğun service account'a tıkla
   - "KEYS" sekmesine git
   - "ADD KEY" > "Create new key"
   - "JSON" seç
   - "CREATE" tıkla
   - İndirilen JSON dosyasını `d:\KuranTaskent\google-credentials.json` olarak kaydet

5. **.env Güncelle**:
   - `.env` dosyasını aç
   - Ekle: `GOOGLE_APPLICATION_CREDENTIALS=d:\KuranTaskent\google-credentials.json`
