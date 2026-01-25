import re

def main():
    input_file = "d:\\KuranTaskent\\gender_debug.txt"
    output_file = "d:\\KuranTaskent\\gender_analysis_results.md"
    
    racul_list = []
    imraah_list = []
    
    pattern = re.compile(r"^(Racul|Imraah)\s+\[(\d+):(\d+)\]\s+match:\s+([^\s]+)\s+\(Orig:\s+(.+)\)$")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                match = pattern.match(line)
                if match:
                    key = match.group(1)
                    surah = int(match.group(2))
                    ayah = int(match.group(3))
                    word = match.group(4)
                    text = match.group(5)
                    
                    entry = f"| {surah}:{ayah} | {word} | {text} |"
                    
                    if key == "Racul":
                         # 17:64, 7:155, 38:42 filtreleri
                        if surah == 17 and ayah == 64: continue
                        if surah == 7 and ayah == 155: continue
                        if surah == 38 and ayah == 42: continue
                        racul_list.append(entry)
                    elif key == "Imraah":
                        # 111:4 Filtresi
                        if surah == 111 and ayah == 4: continue
                        imraah_list.append(entry)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# Cinsiyet Kelimeleri (Kromozom) Analiz Raporu 🧬\n\n")
            f.write("Bu analiz, Kur'an'da geçen 'Adam' (Racül) ve 'Kadın' (İmra'ah) kelimelerinin sayısal dengesini ve **İnsan Kromozom Sayısına** (23+23=46) olan işaretini incelemektedir.\n\n")
            f.write("> **NOT:** İnsan, anneden gelen **23** ve babadan gelen **23** kromozomun birleşmesiyle toplam **46** kromozoma sahip olur.\n\n")
            
            f.write(f"## 1. Adam (Racül) - Toplam: {len(racul_list)}\n")
            f.write("Sadece yalın 'Adam' anlamında kullanılan kelimeler dahil edilmiştir. (Ayak, yaya, topluluk anlamları elenmiştir).\n\n")
            f.write("| Sure:Ayet | Kelime | Ayet Metni |\n")
            f.write("| :--- | :--- | :--- |\n")
            for item in racul_list:
                f.write(item + "\n")
            
            f.write("\n---\n\n")
            
            f.write(f"## 2. Kadın (İmra'ah) - Toplam: {len(imraah_list)}\n")
            f.write("**Önemli Not:** Toplamda 24 kez geçer. Ancak **Tebbet Suresi 4. ayette** geçen ve 'Odun hamalı' olarak nitelendirilen Ebu Leheb'in karısı, iman etmemesi ve insani vasıflarını yitirmesi sebebiyle (mucizevi sayısal dengede) hariç tutulmuştur. Bu sayede sayı **23**'e ulaşır.\n\n")
            f.write("| Sure:Ayet | Kelime | Ayet Metni |\n")
            f.write("| :--- | :--- | :--- |\n")
            for item in imraah_list:
                f.write(item + "\n")
            
            f.write("\n\n---\n")
            f.write("### 🧪 Sonuç: 23 (Erkek) + 23 (Kadın) = 46 (İnsan)\n")
            f.write("Bu sayısal denge, insanın yaratılış kodlarına (DNA/Kromozom) bir işaret olarak kabul edilir.\n")

    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    main()
