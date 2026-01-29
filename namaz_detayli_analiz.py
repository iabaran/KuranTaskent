import json
import sys

# UTF-8 encoding için
sys.stdout.reconfigure(encoding='utf-8')

# Kuran verilerini yükle
with open('quran_arabic.json', 'r', encoding='utf-8') as f:
    quran_data = json.load(f)

print("=" * 100)
print(" " * 30 + "NAMAZ HAKKINDA KUR'AN ANALİZİ")
print("=" * 100)
print()

# ============================================================================
# BÖLÜM 0: AKIL VE DÜŞÜNCE - ATALARI KÖRÜ KÖRÜNE TAKİP ETMEME
# ============================================================================
print("🧠 " + "=" * 95)
print("0️⃣  AKIL, DÜŞÜNCE VE ATALARI KÖRÜ KÖRÜNE TAKİP ETMEME")
print("=" * 100)
print("""
📖 Kur'an, körü körüne atalara uymamayı ve AKIL ile hareket etmeyi emreder:

""")

# Akıl ve atalar hakkında ayetleri ara
akil_keywords = ['تَعۡقِلُونَ', 'يَعۡقِلُونَ', 'تَتَفَكَّرُونَ', 'يَتَفَكَّرُونَ', 'أَفَلَا تَعۡقِلُونَ', 'لِّقَوۡمٖ يَعۡقِلُونَ']
atalar_keywords = ['ءَابَآءَنَآ', 'ءَابَآؤُنَآ', 'ءَابَآئِنَآ']

akil_ayetleri = []
atalar_ayetleri = []

for surah in quran_data:
    surah_number = surah['id']
    surah_name = surah['name']
    surah_name_tr = surah.get('transliteration', '')
    
    for ayah in surah['verses']:
        ayah_number = ayah['id']
        ayah_text = ayah['text']
        
        # Akıl/düşünce ayetleri
        for keyword in akil_keywords:
            if keyword in ayah_text:
                if not any(a['surah_number'] == surah_number and a['ayah_number'] == ayah_number for a in akil_ayetleri):
                    akil_ayetleri.append({
                        'surah_number': surah_number,
                        'surah_name': surah_name,
                        'surah_name_tr': surah_name_tr,
                        'ayah_number': ayah_number,
                        'ayah_text': ayah_text,
                    })
                break
        
        # Atalar ayetleri
        for keyword in atalar_keywords:
            if keyword in ayah_text:
                if not any(a['surah_number'] == surah_number and a['ayah_number'] == ayah_number for a in atalar_ayetleri):
                    atalar_ayetleri.append({
                        'surah_number': surah_number,
                        'surah_name': surah_name,
                        'surah_name_tr': surah_name_tr,
                        'ayah_number': ayah_number,
                        'ayah_text': ayah_text,
                    })
                break

print(f"🧠 AKIL VE DÜŞÜNCE ('aklınızı kullanmaz mısınız?') - {len(akil_ayetleri)} ayet bulundu:")
print("-" * 100)
# Sadece ilk 5 tanesini göster
for i, ayah in enumerate(akil_ayetleri[:5], 1):
    print(f"{i}. {ayah['surah_name']} ({ayah['surah_name_tr']}) - Ayet {ayah['ayah_number']}")
    print(f"   📖 {ayah['ayah_text'][:150]}...")
    print()
print(f"   ... ve {len(akil_ayetleri)-5} ayet daha (toplam {len(akil_ayetleri)} ayet)")

print()
print(f"⚠️ ATALARI KÖRÜ KÖRÜNE TAKİP ETMEME - {len(atalar_ayetleri)} ayet bulundu:")
print("-" * 100)
for i, ayah in enumerate(atalar_ayetleri[:5], 1):
    print(f"{i}. {ayah['surah_name']} ({ayah['surah_name_tr']}) - Ayet {ayah['ayah_number']}")
    print(f"   📖 {ayah['ayah_text'][:150]}...")
    print()
print(f"   ... ve {len(atalar_ayetleri)-5} ayet daha (toplam {len(atalar_ayetleri)} ayet)")

print("""
💡 ÖNEMLİ MESAJ:
   Kur'an, "Atalarımızı böyle bulduk" diyerek körü körüne takip etmeyi eleştirir.
   AKIL ve DÜŞÜNCE ile hareket etmeyi, her şeyi sorgulamayı teşvik eder.
   Bu, dini pratiklerde de geçerlidir.
""")

# ============================================================================
# BÖLÜM 1: NAMAZIN ÖZÜNÜ ANLATAN AYETLER
# ============================================================================
print("=" * 100)
print("1️⃣  NAMAZIN ÖZÜ: ALLAH'A YÖNELİŞ VE ZİKİR")
print("=" * 100)

# Öz ile ilgili ayetler - özellikle zikir, huşu, kalp ile ilgili
oz_keywords = ['ذِكۡرِي', 'لِذِكۡرِيٓ', 'خَٰشِعُونَ', 'خَٰشِعِينَ', 'قَانِتِينَ', 'تَنۡهَىٰ عَنِ ٱلۡفَحۡشَآءِ']

oz_ayetleri = []
for surah in quran_data:
    for ayah in surah['verses']:
        for keyword in oz_keywords:
            if keyword in ayah['text']:
                if not any(a['surah_number'] == surah['id'] and a['ayah_number'] == ayah['id'] for a in oz_ayetleri):
                    oz_ayetleri.append({
                        'surah_number': surah['id'],
                        'surah_name': surah['name'],
                        'surah_name_tr': surah.get('transliteration', ''),
                        'ayah_number': ayah['id'],
                        'ayah_text': ayah['text'],
                    })
                break

print("""
📖 Kur'an namazın ÖZÜNÜ şöyle tanımlar:

""")

# Önemli ayetler
important_verses = [
    (20, 14, "Taha 14 - Namazın Amacı"),  # Beni anmak için namaz kıl
    (29, 45, "Ankebut 45 - Namazın Faydası"),  # Namaz kötülükten alıkoyar
    (23, 2, "Muminun 2 - Namazda Huşu"),  # Namazında huşu içinde olanlar
]

for surah_id, ayah_id, title in important_verses:
    for surah in quran_data:
        if surah['id'] == surah_id:
            for ayah in surah['verses']:
                if ayah['id'] == ayah_id:
                    print(f"⭐ {title}")
                    print(f"   📖 {ayah['text']}")
                    print()

print("""
💡 NAMAZIN ÖZÜ:
   ┌────────────────────────────────────────────────────────────────────┐
   │  1. ALLAH'I ANMAK (Zikir)                                          │
   │  2. HUŞU İÇİNDE OLMAK (Kalp ile bağlantı)                          │
   │  3. KÖTÜLÜKTEN ALIKOYULMAK (Ahlaki gelişim)                        │
   │  4. ALLAH'A YÖNELİŞ (Doğru niyet)                                  │
   │  5. ANLAYARAK KILMAK (Bilinçli ibadet)                             │
   └────────────────────────────────────────────────────────────────────┘
   
   ❌ Rekat sayısı Kur'an'da belirtilmez!
   ✅ Önemli olan NASIL kıldığın, ne kadar ANLADIĞIN ve ne kadar HUŞU içinde olduğundur.
""")

# ============================================================================
# BÖLÜM 2: NAMAZ VAKİTLERİ
# ============================================================================
print("=" * 100)
print("2️⃣  NAMAZ VAKİTLERİ (Kur'an'dan)")
print("=" * 100)

vakit_ayetleri = [
    (11, 114, "Hud 114"),  # Gündüzün iki ucunda ve gecenin yakın saatlerinde
    (17, 78, "İsra 78"),  # Güneşin batıya meyletmesinden gecenin karanlığına kadar
    (24, 58, "Nur 58"),  # Sabah namazından önce, öğle sıcağında, yatsı namazından sonra
    (30, 17, "Rum 17-18"),  # Akşam ve sabah
]

for surah_id, ayah_id, title in vakit_ayetleri:
    for surah in quran_data:
        if surah['id'] == surah_id:
            for ayah in surah['verses']:
                if ayah['id'] == ayah_id:
                    print(f"\n📖 {title}:")
                    print(f"   {ayah['text']}")

print("""

💡 KUR'AN'DA NAMAZ VAKİTLERİ:
   • Sabah namazı (Fecr/Fecir)
   • Gündüzün iki ucu (sabah ve akşam)
   • Gecenin yakın saatleri
   • Güneşin batıya meyli ile gecenin karanlığı arası
   
   ⚠️ NOT: Kur'an vakitleri belirtir ama kaç vakit olduğunu 
         veya her vakitte kaç rekat kılınacağını SÖYLEMEZ!
""")

# ============================================================================
# BÖLÜM 3: NAMAZIN KILINIŞI
# ============================================================================
print("=" * 100)
print("3️⃣  NAMAZIN KILINIŞI (Rükû, Secde)")
print("=" * 100)

print("""
📖 Kur'an'da namazın fiziksel hareketleri:

   • RÜKÛ (Eğilme): "Rükû edenlerle birlikte rükû edin" (Bakara 43)
   • SECDE (Yere kapanma): Birçok ayette geçer
   • KIYAM (Ayakta durma): "Allah'a boyun eğerek ayakta durun" (Bakara 238)
   • KIBLE (Kabe'ye yönelme): "Mescid-i Haram'a yönel" (Bakara 144)

💡 ANCAK:
   ❌ Kaç kez rükû yapılacağı belirtilmez
   ❌ Kaç kez secde edileceği belirtilmez
   ❌ Kaç rekat kılınacağı belirtilmez
   ❌ Her rekatta ne okunacağı detaylandırılmaz
   
   ✅ Bunlar Kur'an'da yok çünkü ÖNEMLİ OLAN:
      - Allah'ı anmak
      - Huşu içinde olmak
      - Anlayarak kılmak
      - Vakitlerinde dosdoğru kılmak
""")

# ============================================================================
# BÖLÜM 4: SAVAŞ/KORKU NAMAZI
# ============================================================================
print("=" * 100)
print("4️⃣  SAVAŞ/KORKU NAMAZI (Nisa 101-102)")
print("=" * 100)

for surah in quran_data:
    if surah['id'] == 4:
        for ayah in surah['verses']:
            if ayah['id'] == 101:
                print(f"\n📖 Nisa 101:")
                print(f"   {ayah['text']}")
            if ayah['id'] == 102:
                print(f"\n📖 Nisa 102:")
                print(f"   {ayah['text']}")

print("""

💡 BU AYETLER NE DİYOR:
   • Yolculukta/savaşta namazı KISALTABİLİRSİNİZ
   • Bu, esneklik olduğunu gösterir
   • Sabit bir rekat sayısı dayatılmaz
   • Duruma göre uyarlama mümkündür
   
   ⚠️ Kur'an'ın mesajı: Namaz KATILAŞMIŞ bir ritüel değil,
      ESNEK ve ANLAMLI bir ibadettir.
""")

# ============================================================================
# BÖLÜM 5: SONUÇ VE GENEL DEĞERLENDİRME
# ============================================================================
print("=" * 100)
print("5️⃣  SONUÇ: NAMAZIN GERÇEK ANLAMI")
print("=" * 100)

print("""
🎯 KUR'AN'IN NAMAZ HAKKINDA SÖYLEDİKLERİ:

   ✅ Namaz FARZ'dır - vaciptir, kılınmalıdır
   ✅ Belirli VAKİTLERDE kılınmalıdır
   ✅ RÜKÛ ve SECDE içerir
   ✅ HUŞU içinde olmalıdır
   ✅ Allah'ı ANMAK içindir (zikir)
   ✅ Kötülükten ALIKOYMALIDIR
   ✅ ANLAYARAK kılınmalıdır
   ✅ DOSDOĞRU kılınmalıdır (ikame)
   
   ❌ KUR'AN'DA OLMAYAN:
   ❌ Kaç rekat kılınacağı
   ❌ Her rekatta ne okunacağı
   ❌ Kaç vakit olduğu (rakam olarak)
   ❌ Namazın dakika cinsinden süresi

🧠 AKIL VE DÜŞÜNCE:

   Kur'an der ki:
   "Onlara 'Allah'ın indirdiğine uyun' denildiğinde, 
   'Hayır, biz atalarımızı üzerinde bulduğumuz şeye uyarız' derler.
   Ya ataları bir şey anlamayan ve doğru yolu bulamayan kimseler idiyseler?"
   (Bakara 170)
   
   💡 Bu ne demek?
   • Körü körüne takip YANLIŞ
   • AKIL ile düşünmek DOĞRU
   • Herkes ANLAYARAK ibadet etmeli
   • Ritüeller amaç değil, ARAÇ'tır
   
🕌 NAMAZIN ÖZÜ:

   ┌────────────────────────────────────────────────────────────────────┐
   │                                                                    │
   │   "Beni anmak için namaz kıl" (Taha 20:14)                         │
   │                                                                    │
   │   Önemli olan:                                                     │
   │   • Allah'a YÖNELİŞ                                                │
   │   • HUŞU ve SAMİMİYET                                              │
   │   • DUA edebilmek                                                  │
   │   • ANLAYARAK kılmak                                               │
   │   • VAKİTLERİNDE kılmak                                            │
   │   • DOSDOĞRU kılmak                                                │
   │                                                                    │
   │   Kimi 2 kılar, kimi 5 kılar, kimi 10 kılar...                     │
   │   Hepsi de kabul olabilir - önemli olan ÖZ!                        │
   │                                                                    │
   └────────────────────────────────────────────────────────────────────┘

📚 KAYNAKLAR:
   • Bakara 170 - Ataları körü körüne takip etmeme
   • Taha 14 - Namazın amacı: Allah'ı anmak
   • Ankebut 45 - Namaz kötülükten alıkoyar
   • Muminun 2 - Namazda huşu
   • Nisa 101-102 - Namazda esneklik

✨ Allah en doğrusunu bilir.
""")

print("=" * 100)
print(f"📊 İSTATİSTİK: Toplam {len(akil_ayetleri)} akıl/düşünce ayeti, {len(atalar_ayetleri)} atalar ayeti analiz edildi.")
print("=" * 100)
