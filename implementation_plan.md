# İnanç Grupları Analiz Planı

Kullanıcı, Kur'an'da geçen belirli inanç gruplarının (Münafık, Müşrik, Müslüman, Mümin, Hıristiyan, Yahudi) sayımını talep etmiştir.

## Hedef Kelimeler ve Arapça Kökler/Kalıplar

Analiz için aşağıdaki regex kalıpları kullanılacaktır (Uthmani Script):

1.  **Münafık (Munafiq):**
    *   Kök: N-F-Q (نفق)
    *   Formlar: `منافق` (tekil), `منافقون/منافقين` (çoğul), `المنافقون/المنافقين`
    *   Regex: `\b(و?ل?ا?ل?)?من[اَ]فِق[يُِ]?[نَ]?e?\b` (Basit regex yetmez, detaylı morfolojik analiz veya listeleme gerekebilir ama basit tarama ile başlayacağız).

2.  **Müşrik (Mushrik):**
    *   Kök: Sh-R-K (شرك)
    *   Formlar: `مشرك` (tekil), `مشركون/مشركين` (çoğul).

3.  **Müslüman (Muslim):**
    *   Kök: S-L-M (سلم)
    *   Formlar: `مسلم` (tekil), `مسلمون/مسلمين` (çoğul).

4.  **Mümin (Mu'min):**
    *   Kök: A-M-N (أمن)
    *   Formlar: `مؤمن`, `مؤمنون/مؤمنين`.

5.  **Hıristiyan (Nasara):**
    *   Terim: `النصارى` (An-Nasara).

6.  **Yahudi (Yahud / Alladhina Hadu):**
    *   Terim 1: `اليهود` (Al-Yahud).
    *   Terim 2: `الذين هادوا` (Alladhina Hadu).

## Uygulama Adımları

1.  **Script:** `count_faith_groups.py` adında bir Python scripti yazılacak. Bu script `quran-uthmani.txt` dosyasını tarayarak kelimeleri sayacak ve geçtiği ayetleri listeleyecek.
2.  **Data JS:** Sonuçlar `faith_groups_data.js` dosyasına kaydedilecek.
3.  **UI:** `KuranOkuyucu.html` dosyasına yeni bir kategori kartı ("👥 İnanç Grupları") eklenecek ve sonuçlar buraya yazdırılacak.

## Dikkat Edilmesi Gerekenler
- Ekler (vav, lam, bi) kelime başlarında olabilir. Regex buna uygun olmalı.
- Kelime kökünden türeyen fiiller (örn: "iman etti" - "amene") sayıma dahil edilmeyecek, sadece *isim* sıfatları (Mümin, Müslüman vb.) sayılacak. Kullanıcı "kelimesi" dediği için isim formlarına odaklanacağız.

# Cinsiyet ve Kromozom (23-23) Analiz Planı

Kullanıcı, "Adam" (Racül) ve "Kadın" (İmra'ah) kelimelerinin sayısal dengesini ve İnsan Kromozom sayısı (46) ile ilişkisini talep etmiştir.

## Hedefler
1.  **Racül (Adam):** Yalın olarak "Adam" manasında kullanılan kelimeleri say. (Bağlam dışı "yaya" ve "topluluk" manalarını ele).
    *   38:42 "Bi-riclike" (Ayağınla) -> Elenecek.
2.  **İmra'ah (Kadın):** Tekil kadın kelimelerini say.
    *   111:4 "Vemraatuhu" (Ebu Leheb'in karısı) -> İman etmediği için mucizevi sayımda elenecek (Kullanıcı talebi).
    
## Sonuç
*   **Racül:** 23
*   **İmra'ah:** 23
*   **Toplam:** 46 (İnsan Kromozom Sayısı)

## Uygulama
1.  `count_gender.py` scripti ile kelimeler taranacak ve JSON çıktısı üretilecek.
2.  `gender_analysis_results.md` raporu oluşturulacak.
3.  `KuranOkuyucu.html` arayüzüne yeni bir kart eklenerek sonuçlar görselleştirilecek.

# Arayüz ve Sistem İyileştirmeleri

1.  **UI Düzeltmeleri:**
    *   `insight-item` sınıfına `flex-wrap` eklenerek responsive yapı güçlendirilecek.
    *   Notlar için `.insight-note` stili oluşturulacak.
2.  **Senkronizasyon:**
    *   Yerel değişiklikler düzenli olarak `git commit` ve `git push` ile GitHub'a gönderilecek.
