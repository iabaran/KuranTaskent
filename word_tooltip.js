// Word-by-Word Tooltip Functionality for Kuran Okuyucu
// Optimized for large JSON data and dynamic UI updates

let wordByWordData = null;
let isDataLoaded = false;
let isLoading = false;
let loadPromise = null;

function updateStatus(msg, isError = false) {
    const statusDiv = document.getElementById('tooltipStatus');
    if (statusDiv) {
        statusDiv.textContent = (isError ? '⚠️ ' : '🔄 ') + msg;
        statusDiv.style.color = isError ? '#e74c3c' : '#7f8c8d';
    }
}

// Load word-by-word JSON data
async function loadWordByWordData() {
    if (isDataLoaded) return true;

    // Bypassing CORS: check if data is already loaded via script tag
    if (window.quranWordByWordData) {
        console.log('✅ Data found in global variable (No CORS issues)');
        wordByWordData = window.quranWordByWordData;
        isDataLoaded = true;
        updateStatus('✅ Kelime mealleri hazır.');
        return true;
    }

    if (isLoading) return loadPromise;

    isLoading = true;
    updateStatus('Veriler yükleniyor (24MB)...');

    loadPromise = (async () => {
        try {
            console.log('📥 Loading word-by-word data (24MB)...');
            const response = await fetch('quran_word_by_word.json');
            if (!response.ok) throw new Error('Kelime meali verisi bulunamadı.');

            wordByWordData = await response.json();
            isDataLoaded = true;
            isLoading = false;
            updateStatus('✅ Kelime mealleri hazır.');
            console.log('✅ Word-by-word data loaded successfully');
            return true;
        } catch (error) {
            console.error('❌ Error loading word-by-word data:', error);
            isLoading = false;
            updateStatus('Yükleme hatası (Yerel dosyayı doğrudan açtığınız için CORS engeli). Lütfen quran_word_by_word.js dosyasının oluştuğundan emin olun.', true);
            return false;
        }
    })();
    return loadPromise;
}

// Get word data for a specific verse
function getVerseWords(surahNumber, verseNumber) {
    if (!wordByWordData) return null;

    const surah = wordByWordData.surahs?.find(s => parseInt(s.surah_number) === parseInt(surahNumber));
    if (!surah) return null;

    const verse = surah.verses?.find(v => parseInt(v.verse_number) === parseInt(verseNumber));
    return verse ? verse.words : null;
}

// Create tooltip HTML for a word with cumulative index
function createWordTooltip(arabicWord, transcription, turkish, currentIndex) {
    const ts = transcription || '---';
    const tr = turkish || '[Meal Bekleniyor]';

    return `<span class="arabic-word">
                ${arabicWord}
                <span class="word-index">${currentIndex}</span>
                <span class="word-tooltip">
                    <div class="tooltip-transcription">${ts}</div>
                    <div class="tooltip-turkish">${tr}</div>
                </span>
            </span>`;
}

// Process Arabic text and add tooltips for a single verse
function processVerseWithTooltips(arabicText, surahNumber, verseNumber, startCounter) {
    // Kur'an durak işaretleri (bunlar kelime listesinde bulunmaz, pas geçilmeli)
    const QURAN_SYMBOLS = /[\u06D6-\u06DC\u06DF-\u06E8\u06EA-\u06ED]/;

    let words = getVerseWords(surahNumber, verseNumber);
    let counter = startCounter;

    // Eğer veri yoksa veya Besmele başlığı ise manuel eşleme dene
    if (!words || words.length === 0) {
        if (arabicText.includes("بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ")) {
            const basmalaWords = [
                { arabic: "بِسْمِ", transcription: "bi-smi", turkish: "adıyla" },
                { arabic: "ٱللَّهِ", transcription: "llāhi", turkish: "Allah'ın" },
                { arabic: "ٱلرَّحْمَٰنِ", transcription: "r-raḥmāni", turkish: "Rahmân" },
                { arabic: "ٱلرَّحِيمِ", transcription: "r-raḥīm", turkish: "Rahîm" }
            ];
            words = basmalaWords;
        } else {
            const tempWords = arabicText.trim().split(/\s+/);
            const result = tempWords.map((word) => {
                const html = `<span class="arabic-word">${word}<span class="word-index">${counter}</span></span>`;
                counter++;
                return html;
            }).join(' ');
            return { html: result, nextCounter: counter };
        }
    }

    const arabicWords = arabicText.trim().split(/\s+/);
    let result = '';
    let dataIndex = 0; // Veri listesindeki gerçek kelime endeksi

    for (let i = 0; i < arabicWords.length; i++) {
        const arabicWord = arabicWords[i];

        // Eğer kelime sadece bir Kur'an sembolü ise tooltip ekleme ve veri endeksini artırma
        if (arabicWord.length <= 2 && QURAN_SYMBOLS.test(arabicWord)) {
            result += `<span class="arabic-symbol">${arabicWord}</span>`;
        } else {
            const wordData = words[dataIndex] || null;

            if (wordData) {
                result += createWordTooltip(
                    arabicWord,
                    wordData.transcription,
                    wordData.turkish,
                    counter
                );
            } else {
                result += `<span class="arabic-word">${arabicWord}<span class="word-index">${counter}</span></span>`;
            }

            dataIndex++; // Sadece gerçek kelime bulduğumuzda veri endeksini artır
            counter++;   // Sadece gerçek kelime bulduğumuzda kelime sayısını artır
        }

        if (i < arabicWords.length - 1) {
            result += ' ';
        }
    }

    return { html: result, nextCounter: counter };
}

// Global initialization function
window.initWordTooltips = async function () {
    console.log('🔄 Initializing cumulative word counter...');

    // Verilerin yüklendiğinden emin ol
    if (!isDataLoaded) {
        const loaded = await loadWordByWordData();
        if (!loaded) return;
    }

    const surahSelect = document.getElementById('surahSelect');
    const surahNumber = surahSelect ? parseInt(surahSelect.value) : null;
    if (!surahNumber) return;

    // Hedef alanları bul (ayet kartları ve besmele başlıkları)
    // ÖNEMLİ: Sıralama DOM sırasına göre olmalı ki sayaç düzgün devam etsin
    const allVerses = document.querySelectorAll('.basmala-header, .verse-card .arabic-line');

    let surahWordCounter = 1;

    allVerses.forEach((arabicLine) => {
        // Eğer zaten işlendiyse bile sayaç için kelime sayısını almamız veya baştan başlamamız lazım
        // Bu yüzden her seferinde data-tooltipped kontrolü yapıp ama sayacı HEP güncel tutarak ilerliyoruz

        let verseNumber;
        if (arabicLine.classList.contains('basmala-header')) {
            verseNumber = 1;
        } else {
            verseNumber = parseInt(arabicLine.getAttribute('data-ayah'));
        }

        const originalText = (arabicLine.getAttribute('data-original-text') || arabicLine.textContent).trim();

        // Orijinal metni sakla (re-init durumlarında silinmesin)
        if (!arabicLine.getAttribute('data-original-text')) {
            arabicLine.setAttribute('data-original-text', originalText);
        }

        if (originalText && !isNaN(verseNumber)) {
            const result = processVerseWithTooltips(originalText, surahNumber, verseNumber, surahWordCounter);

            // Sadece daha önce işlenmemişse HTML'i güncelle
            if (arabicLine.getAttribute('data-tooltipped') !== 'true') {
                arabicLine.innerHTML = result.html;
                arabicLine.setAttribute('data-tooltipped', 'true');
            }

            // Sayaç her durumda ilerlemeli
            surahWordCounter = result.nextCounter;
        }
    });

    console.log(`✅ Cumulative counter complete for Surah ${surahNumber}. Total words: ${surahWordCounter - 1}`);
};

// Sayfa ilk yüklendiğinde veriyi çekmeye başla
document.addEventListener('DOMContentLoaded', () => {
    loadWordByWordData();
});
