import json
import collections
import sys

def analyze_chars():
    try:
        with open('quran_arabic.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: quran_arabic.json not found")
        return

    fatiha = data[0]
    all_text = " ".join(v['text'] for v in fatiha['verses'])
    
    # 1. Traditional Letter Count (Strict Script)
    # Characters that are counted as "letters" in Arabic (Abjad)
    # Alif (including Wasla), Ba, Ta, Tha, Jeem, Ha, Kha, Dal, Thal, Ra, Zay, Seen, Sheen, Sad, Dad, Tah, Zah, Ain, Ghain, Fa, Qaf, Kaf, Lam, Meem, Noon, Ha, Waw, Ya
    # Hamzas are usually counted as the carrier (Alif, Waw, Ya) or sometimes separately.
    
    # Let's count EVERY unicode character first to see what we have
    char_counts = collections.Counter(all_text)
    
    print("Character breakdown in Fatiha:")
    for char, count in sorted(char_counts.items(), key=lambda x: x[1], reverse=True):
        if char == ' ':
            print(f"  Space: {count}")
            continue
        print(f"  {char} (U+{ord(char):04X}): {count}")

    # Specific Letter Counting (Uthmanic Script style)
    # 1. Alif (ا), Alif Wasla (ٱ), Alif Maqsura (ى - if used as alif)
    # 2. Ba (ب)
    # 3. Ta (ت), Marbuta (ة - usually counted as T or H depending on context, but in Fatiha?)
    # ...
    
    # Let's use a more inclusive list of "letters"
    # Hamzas: ء أ ؤ إ ئ (U+0621 to U+0626)
    # Alif: ا (U+0627)
    # Alif Wasla: ٱ (U+0671)
    # Letters: ب to ي (U+0628 to U+064A)
    # Also Alef Superscript (Dagger Alif): ٰ (U+0670) -> often counted in 143, omitted in 139.
    
    letters_only = []
    for char in all_text:
        if 0x0621 <= ord(char) <= 0x063A or 0x0641 <= ord(char) <= 0x064A or ord(char) == 0x0671:
            letters_only.append(char)
        elif ord(char) == 0x0670:
            # Dagger Alif - we'll track it separately
            pass

    print("\nStrict Letter Count (Excluding Dagger Alif and Diacritics):")
    print(f"Total: {len(letters_only)}")
    
    # Let's count with Dagger Alif
    dagger_alifs = all_text.count('\u0670')
    print(f"Dagger Alifs (ٰ): {dagger_alifs}")
    print(f"Total with Dagger Alifs: {len(letters_only) + dagger_alifs}")

if __name__ == "__main__":
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
    analyze_chars()
