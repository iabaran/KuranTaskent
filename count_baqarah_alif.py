
import json

# Define the Alif characters to look for
alif_chars = {
    "0627": "ا (Alef)",
    "0623": "أ (Alef with Hamza Above)",
    "0625": "إ (Alef with Hamza Below)",
    "0622": "آ (Alef with Madda Above)",
    "0671": "ٱ (Alef Wasla)",
    "0670": "ٰ (Superscript Alef)",
}

# Also tracking Alef Maqsura just in case
extra_chars = {
    "0649": "ى (Alef Maqsura)"
}

def count_chars(text, description):
    counts = {k: 0 for k in alif_chars}
    counts_extra = {k: 0 for k in extra_chars}
    
    total_alif = 0
    
    for char in text:
        cp = ord(char)
        hex_cp = f"{cp:04x}"
        if hex_cp in alif_chars:
            counts[hex_cp] += 1
            total_alif += 1
        elif hex_cp in extra_chars:
            counts_extra[hex_cp] += 1
            
    print(f"\n--- {description} ---")
    print(f"Total Length: {len(text)}")
    print("Alif Counts:")
    
    # Initialize grand total
    grand_total_all = 0
    
    for code, _ in alif_chars.items():
        count = counts[code]
        grand_total_all += count
        print(f"  {code}: {count}")
    
    print("\nExtra (Alef Maqsura):")
    for code, _ in extra_chars.items():
        count = counts_extra[code]
        grand_total_all += count
        print(f"  {code}: {count}")
    
    print(f"\nTotal 'Inclusive' Alifs (All types above combined): {grand_total_all}")
    return counts, grand_total_all

def main():
    try:
        with open('d:/KuranTaskent/quran_arabic.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Get Surah Baqarah (ID 2)
        baqarah = next((s for s in data if s['id'] == 2), None)
        if not baqarah:
            print("Error: Surah Baqarah not found.")
            return

        # Get Fatiha (ID 1) to get Basmala text
        fatiha = next((s for s in data if s['id'] == 1), None)
        # Verse 1 of Fatiha is the Basmala
        basmala = fatiha['verses'][0]['text']
        
        # print(f"Basmala Text: {basmala}") # Commented out to avoid encoding error
        
        baqarah_text = ""
        for verse in baqarah['verses']:
            baqarah_text += verse['text']
            
        full_text = basmala + baqarah_text
        
        print("\nAnalyzing Surah Baqarah (including Basmala at start)...")
        count_chars(full_text, "Full Text (Basmala + Baqarah Verses)")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
