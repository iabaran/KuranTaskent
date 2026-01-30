import json
import sys

# UTF-8 encoding için
sys.stdout.reconfigure(encoding='utf-8')

print("Script başlatılıyor...")

# Kuran verilerini yükle
try:
    with open('quran_arabic.json', 'r', encoding='utf-8') as f:
        quran_data = json.load(f)
    print("quran_arabic.json yüklendi.")
except Exception as e:
    print(f"HATA: quran_arabic.json yüklenemedi: {e}")
    sys.exit(1)

# Türkçe meal için - GLOBAL_QURAN_TR formatında
try:
    with open('quran_tr_js.js', 'r', encoding='utf-8') as f:
        tr_content = f.read()
        # "const GLOBAL_QURAN_TR = " kısmını kaldır
        tr_content = tr_content.replace('const GLOBAL_QURAN_TR = ', '').strip()
        # Eğer varsa noktalı virgülü kaldır
        if tr_content.endswith(';'):
            tr_content = tr_content[:-1]
        quran_tr = json.loads(tr_content)
    print("quran_tr_js.js yüklendi.")
except Exception as e:
    print(f"HATA: quran_tr_js.js yüklenemedi veya parse edilemedi: {e}")
    sys.exit(1)

# ============================================================================
# AKIL/DÜŞÜNCE KELİMELERİ
# ============================================================================
akil_keywords = {
    'ya\'qilun': ['يَعۡقِلُونَ', 'تَعۡقِلُونَ'],  # Akletmek
    'yatafakkarun': ['يَتَفَكَّرُونَ', 'تَتَفَكَّرُونَ', 'يَتَفَكَّرُ'],  # Düşünmek
    'yatadabbarun': ['يَتَدَبَّرُونَ', 'تَتَدَبَّرُونَ'],  # Tefekkür etmek
    'ya\'lamun': ['يَعۡلَمُونَ', 'تَعۡلَمُونَ'],  # Bilmek
    'yafqahun': ['يَفۡقَهُونَ', 'تَفۡقَهُونَ'],  # Anlamak/Kavramak
    'ulul_albab': ['أُوْلِي ٱلۡأَلۡبَٰبِ', 'أُوْلُواْ ٱلۡأَلۡبَٰبِ'],  # Akıl sahipleri
}

# Atalar ayetleri
atalar_keywords = ['ءَابَآءَنَا', 'ءَابَآؤُنَا', 'ءَابَآئِنَا', 'ءَابَآئِهِمۡ']

# ============================================================================
# NAMAZ KELİMELERİ
# ============================================================================
namaz_keywords = {
    'salat_genel': ['صَلَوٰة', 'صَلَاة', 'الصَّلَوٰةَ', 'صَلَوٰتِ', 'صَلَاتِهِمۡ'],
    'salat_fiil': ['صَلَّىٰ', 'يُصَلِّ', 'صَلُّواْ', 'فَصَلِّ'],
    'ruku': ['رُكَّعِ', 'ٱرۡكَعُ', 'رَاكِعِ', 'رَٰكِعُونَ'],
    'secde': ['سُجُودِ', 'ٱسۡجُدُ', 'سَاجِدِ', 'سَٰجِدُونَ'],
    'husu': ['خَٰشِعِينَ', 'خَٰشِعُونَ'],
    'vakit': ['ٱلۡفَجۡرِ', 'ٱلۡعِشَآءِ', 'طُلُوعِ', 'غُرُوبِ'],
}

# ============================================================================
# ANALİZ FONKSİYONLARI
# ============================================================================

def get_turkish_translation(surah_id, ayah_id):
    """Türkçe meali al - GLOBAL_QURAN_TR formatı için (Nested dict yapısı)"""
    surah_str = str(surah_id)
    ayah_str = str(ayah_id)
    
    # Yeni format: { "1": { "ayahs": { "1": "..." } } }
    if surah_str in quran_tr:
        surah_obj = quran_tr[surah_str]
        if 'ayahs' in surah_obj and ayah_str in surah_obj['ayahs']:
            return surah_obj['ayahs'][ayah_str]
            
    return "Meal bulunamadı"

def find_verses_with_keywords(keywords_dict, category_name):
    """Belirli anahtar kelimeleri içeren ayetleri bul"""
    results = []
    
    for surah in quran_data:
        surah_number = surah['id']
        surah_name = surah['name']
        surah_name_tr = surah.get('transliteration', '')
        
        for ayah in surah['verses']:
            ayah_number = ayah['id']
            ayah_text = ayah['text']
            
            # Ayet zaten eklendiyse tekrar ekleme (farklı keywordler aynı ayette olabilir)
            is_added = False
            
            for key, patterns in keywords_dict.items():
                if is_added: break
                for pattern in patterns:
                    if pattern in ayah_text:
                        results.append({
                            'surah': surah_number,
                            'ayah': ayah_number,
                            'surahName': surah_name,
                            'surahNameTr': surah_name_tr,
                            'arabic': ayah_text,
                            'turkish': get_turkish_translation(surah_number, ayah_number),
                            'keyword': key,
                            'pattern': pattern
                        })
                        is_added = True
                        break
    
    return results

def find_atalar_verses():
    """Atalar ile ilgili ayetleri bul"""
    results = []
    
    for surah in quran_data:
        surah_number = surah['id']
        surah_name = surah['name']
        surah_name_tr = surah.get('transliteration', '')
        
        for ayah in surah['verses']:
            ayah_number = ayah['id']
            ayah_text = ayah['text']
            
            for pattern in atalar_keywords:
                if pattern in ayah_text:
                    if not any(r['surah'] == surah_number and r['ayah'] == ayah_number for r in results):
                        results.append({
                            'surah': surah_number,
                            'ayah': ayah_number,
                            'surahName': surah_name,
                            'surahNameTr': surah_name_tr,
                            'arabic': ayah_text,
                            'turkish': get_turkish_translation(surah_number, ayah_number),
                            'keyword': 'atalar',
                            'pattern': pattern
                        })
                    break
    
    return results

# ============================================================================
# VERİLERİ TOPLA
# ============================================================================

print("Akıl ayetleri aranıyor...")
akil_verses = find_verses_with_keywords(akil_keywords, 'akil')
print(f"  Toplam {len(akil_verses)} akıl/düşünce ayeti bulundu")

print("Atalar ayetleri aranıyor...")
atalar_verses = find_atalar_verses()
print(f"  Toplam {len(atalar_verses)} atalar ayeti bulundu")

print("Namaz ayetleri aranıyor...")
namaz_verses = find_verses_with_keywords(namaz_keywords, 'namaz')
print(f"  Toplam {len(namaz_verses)} namaz ayeti bulundu")

# ============================================================================
# JS DOSYASI OLUŞTUR (Chunked Write)
# ============================================================================

output_file = 'akil_namaz_data.js'

try:
    with open(output_file, 'w', encoding='utf-8') as f:
        # Header
        f.write("// Akıl, Düşünce ve Namaz Verileri\n")
        f.write("// Otomatik oluşturuldu\n\n")
        
        # 1. AKIL DATA
        f.write("var akilData = {\n")
        f.write('    title: "Akıl ve Düşünce",\n')
        f.write('    description: "Kuran\'da akıl kullanmayı ve düşünmeyi teşvik eden ayetler",\n')
        f.write('    icon: "🧠",\n')
        f.write(f'    totalCount: {len(akil_verses)},\n')
        f.write('    categories: {\n')
        
        # Kategoriler (statik sayıları hesapla)
        counts = {k: 0 for k in akil_keywords.keys()}
        for v in akil_verses:
            if v['keyword'] in counts: counts[v['keyword']] += 1
            
        f.write('        "ya\'qilun": { name: "Akletmek (عقل)", description: "Aklı kullanmak, anlamak", count: ' + str(counts['ya\'qilun']) + ' },\n')
        f.write('        "yatafakkarun": { name: "Tefekkür (فكر)", description: "Derin düşünmek", count: ' + str(counts['yatafakkarun']) + ' },\n')
        f.write('        "ya\'lamun": { name: "Bilmek (علم)", description: "Bilgi sahibi olmak", count: ' + str(counts.get('ya\'lamun', 0)) + ' },\n')
        f.write('        "yafqahun": { name: "Kavramak (فقه)", description: "Derinlemesine anlamak", count: ' + str(counts['yafqahun']) + ' },\n')
        f.write('        "ulul_albab": { name: "Akıl Sahipleri (أولو الألباب)", description: "Derin düşünen insanlar", count: ' + str(counts['ulul_albab']) + ' }\n')
        f.write('    },\n')
        
        f.write('    verses: ')
        # Ayetleri dump et
        f.write(json.dumps(akil_verses, ensure_ascii=False, indent=2))
        f.write('\n};\n\n')
        
        # 2. ATALAR DATA
        f.write("var atalarData = {\n")
        f.write('    title: "Atalar ve Gelenek",\n')
        f.write('    description: "Kuran\'da ataları körü körüne takip etmeme uyarıları",\n')
        f.write('    icon: "⚠️",\n')
        f.write(f'    totalCount: {len(atalar_verses)},\n')
        f.write('    message: "Kuran, \'Atalarımızı böyle bulduk\' diyerek körü körüne takip etmeyi eleştirir",\n')
        f.write('    verses: ')
        f.write(json.dumps(atalar_verses, ensure_ascii=False, indent=2))
        f.write('\n};\n\n')
        
        # 3. NAMAZ DATA
        f.write("var namazData = {\n")
        f.write('    title: "Namaz Hakkında",\n')
        f.write('    description: "Kuran\'da namaz ile ilgili tüm bilgiler",\n')
        f.write('    icon: "🕌",\n')
        f.write(f'    totalCount: {len(namaz_verses)},\n')
        f.write('    importantNote: "Kuran\'da namazın özü Allah\'ı anmak, O\'na yalvarmak ve doğru yola yönelmektir. Kuran, namazın ruhunu ve önemini vurgularken, aklı kullanmayı ve körü körüne taklitten kaçınmayı emreder.",\n')
        f.write('    categories: {\n')
        
        # Namaz Kategorileri
        n_counts = {k: 0 for k in namaz_keywords.keys()}
        for v in namaz_verses:
            if v['keyword'] in n_counts: n_counts[v['keyword']] += 1

        f.write('        "salat_genel": { name: "Salat/Namaz (صلاة)", description: "Genel namaz ifadeleri", count: ' + str(n_counts['salat_genel']) + ' },\n')
        f.write('        "salat_fiil": { name: "Namaz Kılmak (صلى)", description: "Namaz kılma fiilleri", count: ' + str(n_counts['salat_fiil']) + ' },\n')
        f.write('        "ruku": { name: "Rükû (ركوع)", description: "Eğilme/Rükû", count: ' + str(n_counts['ruku']) + ' },\n')
        f.write('        "secde": { name: "Secde (سجود)", description: "Yere kapanma/Secde", count: ' + str(n_counts['secde']) + ' },\n')
        f.write('        "husu": { name: "Huşu (خشوع)", description: "Kalp ile bağlantı", count: ' + str(n_counts['husu']) + ' },\n')
        f.write('        "vakit": { name: "Vakitler", description: "Namaz vakitleri", count: ' + str(n_counts['vakit']) + ' }\n')
        f.write('    },\n')
        
        f.write('    keyVerses: [\n')
        f.write('        {surah: 20, ayah: 14, title: "Namazın Amacı", text: "Beni anmak için namaz kıl"},\n')
        f.write('        {surah: 29, ayah: 45, title: "Namazın Faydası", text: "Namaz kötülükten alıkoyar"},\n')
        f.write('        {surah: 4, ayah: 101, title: "Savaş Namazı", text: "Yolculukta namazı kısaltabilirsiniz"},\n')
        f.write('        {surah: 4, ayah: 102, title: "Korku Namazı", text: "Savaşta cemaat iki gruba ayrılır"},\n')
        f.write('        {surah: 23, ayah: 2, title: "Namazda Huşu", text: "Namazlarında huşu içinde olanlar"}\n')
        f.write('    ],\n')
        
        f.write('    verses: ')
        f.write(json.dumps(namaz_verses, ensure_ascii=False, indent=2))
        f.write('\n};\n')

    print(f"\n✅ {output_file} dosyası başarıyla oluşturuldu!")
    print(f"\nÖZET:")
    print(f"  🧠 Akıl/Düşünce: {len(akil_verses)}")
    print(f"  ⚠️ Atalar: {len(atalar_verses)}")
    print(f"  🕌 Namaz: {len(namaz_verses)}")
    print(f"  📁 Dosya Yolu: {output_file}")

except Exception as e:
    print(f"HATA: Dosya oluşturulurken hata: {e}")
    sys.exit(1)
