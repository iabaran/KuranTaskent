"""
HTML Kuran Okuyucu Oluşturucu
İndirilen JSON verilerini kullanarak modern, tek sayfalık bir HTML Kuran okuyucusu oluşturur.
"""

import json
from pathlib import Path

def create_html_reader():
    print("HTML okuyucu oluşturuluyor...")
    
    # Verileri yükle
    try:
        with open("quran_data/quran_ar.json", "r", encoding="utf-8") as f:
            quran_ar = json.load(f)
        with open("quran_data/quran_tr.json", "r", encoding="utf-8") as f:
            quran_tr = json.load(f)
    except Exception as e:
        print(f"HATA: Veri dosyaları okunamadı: {e}")
        return

    # HTML Şablonu
    html_content = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kuran-ı Kerim Okuyucu</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Roboto:wght@300;400;700&display=swap');
        
        body {
            font-family: 'Roboto', sans-serif;
            background-color: #f5f5f5;
            margin: 0;
            padding: 0;
            color: #333;
        }
        
        header {
            background-color: #1a5f7a;
            color: white;
            padding: 1rem;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        h1 { margin: 0; font-size: 1.5rem; text-align: center; }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .selector-container {
            background: white;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            text-align: center;
        }
        
        select {
            padding: 10px;
            font-size: 16px;
            border-radius: 4px;
            border: 1px solid #ddd;
            width: 100%;
            max-width: 300px;
        }
        
        .surah-container {
            display: none; /* JS ile açılacak */
        }
        
        .surah-header {
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background: white;
            border-radius: 8px;
            border-bottom: 3px solid #1a5f7a;
        }
        
        .ayah-card {
            background: white;
            margin-bottom: 15px;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            transition: transform 0.2s;
        }
        
        .ayah-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        
        .ayah-number {
            display: inline-block;
            background: #eee;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 12px;
            color: #666;
            margin-bottom: 10px;
        }
        
        .arabic-text {
            font-family: 'Amiri', serif;
            font-size: 28px;
            line-height: 2.2;
            text-align: right;
            direction: rtl;
            color: #000;
            margin-bottom: 15px;
            padding-bottom: 15px;
            border-bottom: 1px solid #f0f0f0;
        }
        
        .translation-text {
            font-size: 16px;
            line-height: 1.6;
            color: #444;
            max-height: 0;
            opacity: 0;
            overflow: hidden;
            transition: all 0.4s ease-in-out;
            margin-top: 0;
        }

        .ayah-card:hover .translation-text {
            max-height: 500px; /* Yeterince büyük bir değer */
            opacity: 1;
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px dashed #ddd;
        }

        .hover-hint {
            font-size: 11px;
            color: #999;
            text-align: center;
            margin-top: 10px;
            font-style: italic;
            opacity: 0.7;
            transition: opacity 0.3s;
        }

        .ayah-card:hover .hover-hint {
            opacity: 0;
            display: none;
        }
        
        .bismillah {
            font-family: 'Amiri', serif;
            text-align: center;
            font-size: 32px;
            margin-bottom: 20px;
            display: block;
        }
    </style>
</head>
<body>

<header>
    <h1>Kuran-ı Kerim Okuyucu</h1>
</header>

<div class="container">
    <div class="selector-container">
        <select id="surahSelect" onchange="loadSurah()">
            <option value="">Sure Seçiniz...</option>
"""
    
    # Sureleri ekle
    # JSON key'leri string olduğu için sıralama sorunu olabilir, int'e çevirip sıralayalım
    sorted_surah_nums = sorted([int(k) for k in quran_ar.keys()])
    
    for num in sorted_surah_nums:
        surah = quran_ar[str(num)]
        name_ar = surah['name']
        name_en = surah['englishName']
        html_content += f'            <option value="{num}">{num}. {name_en} - {name_ar}</option>\n'

    html_content += """
        </select>
    </div>

    <div id="contentArea"></div>
</div>

<script>
    // Verileri JS objesi olarak göm (Büyük veri ama yerel çalışacağı için hızlı olur)
    const quranData = {
        ar: """ + json.dumps(quran_ar, ensure_ascii=False) + """,
        tr: """ + json.dumps(quran_tr, ensure_ascii=False) + """
    };

    function loadSurah() {
        const surahNum = document.getElementById('surahSelect').value;
        const contentDiv = document.getElementById('contentArea');
        
        if (!surahNum) {
            contentDiv.innerHTML = '';
            return;
        }
        
        const surahAr = quranData.ar[surahNum];
        const surahTr = quranData.tr[surahNum];
        
        let html = `
            <div class="surah-header">
                <h2>${surahNum}. ${surahAr.englishName}</h2>
                <div class="arabic-text" style="text-align: center; border: none; font-size: 36px;">
                    ${surahAr.name}
                </div>
            </div>
        `;
        
        // Fatiha (1) ve Tevbe (9) hariç Besmele ekle
        if (surahNum != 1 && surahNum != 9) {
            html += `<div class="bismillah">بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ</div>`;
        }
        
        // Ayetleri listele
        // Ayet numaralarını sırala
        const ayahNums = Object.keys(surahAr.ayahs).map(Number).sort((a,b) => a-b);
        
        ayahNums.forEach(num => {
            const textAr = surahAr.ayahs[num];
            const textTr = surahTr.ayahs[num] || "Çeviri bulunamadı.";
            
            html += `
                <div class="ayah-card">
                    <div class="ayah-number">Ayet ${num}</div>
                    <div class="arabic-text">${textAr}</div>
                    <div class="hover-hint">(Anlamı görmek için üzerine gelin)</div>
                    <div class="translation-text">${textTr}</div>
                </div>
            `;
        });
        
        contentDiv.innerHTML = html;
        window.scrollTo(0, 0);
    }
    
    // Sayfa yüklendiğinde Fatiha'yı aç
    window.onload = function() {
        document.getElementById('surahSelect').value = "1";
        loadSurah();
    }
</script>

</body>
</html>
"""

    with open("KuranOkuyucu.html", "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print("[OK] KuranOkuyucu.html oluşturuldu.")
    print(f"Dosya boyutu: {Path('KuranOkuyucu.html').stat().st_size / 1024 / 1024:.2f} MB")

if __name__ == "__main__":
    create_html_reader()
