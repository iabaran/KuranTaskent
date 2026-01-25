import re

def main():
    input_file = "d:\\KuranTaskent\\gender_debug.txt"
    output_file = "d:\\KuranTaskent\\gender_analysis_results.md"
    
    racul_list = []
    imraah_list = []
    
    # Regex to parse line: "Key [Surah:Ayah] match: Word (Orig: Text)"
    # Example: Racul [2:282] match: فرجل (Orig: ...)
    pattern = re.compile(r"^(Racul|Imraah)\s+\[(\d+):(\d+)\]\s+match:\s+([^\s]+)\s+\(Orig:\s+(.+)\)$")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                match = pattern.match(line)
                if match:
                    key = match.group(1)
                    surah = match.group(2)
                    ayah = match.group(3)
                    word = match.group(4)
                    text = match.group(5)
                    
                    entry = f"| {surah}:{ayah} | {word} | {text} |"
                    
                    if key == "Racul":
                        racul_list.append(entry)
                    elif key == "Imraah":
                        imraah_list.append(entry)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# Cinsiyet Kelimeleri Analiz Sonuçları\n\n")
            f.write("Bu belge, Kur'an'da biyolojik cinsiyeti ve insan türünü ifade eden 'Adam' ve 'Kadın' kelimelerinin geçtiği ayetlerin listesidir.\n\n")
            
            f.write(f"## 1. Adam (Racül) - Toplam: {len(racul_list)}\n")
            f.write("Bağlamdışı kullanımlar (yaya, topluluk) elendikten sonraki net listedir.\n\n")
            f.write("| Sure:Ayet | Kelime | Ayet Metni |\n")
            f.write("| --- | --- | --- |\n")
            for item in racul_list:
                f.write(item + "\n")
            
            f.write("\n---\n\n")
            
            f.write(f"## 2. Kadın (İmra'ah) - Toplam: {len(imraah_list)}\n")
            f.write("Tekil 'Kadın' kelimesinin geçtiği ayetlerdir.\n\n")
            f.write("| Sure:Ayet | Kelime | Ayet Metni |\n")
            f.write("| --- | --- | --- |\n")
            for item in imraah_list:
                f.write(item + "\n")
                
        print(f"Rapor oluşturuldu: {output_file}")
        print(f"Racul: {len(racul_list)}")
        print(f"Imraah: {len(imraah_list)}")

    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    main()
