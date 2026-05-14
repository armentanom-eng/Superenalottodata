import requests
import os
import re

def update_csv():
    file_path = 'storico_completo.csv'
    url = "https://www.superenalotto.net/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    try:
        r = requests.get(url, headers=headers, timeout=20)
        r.encoding = 'utf-8'
        html = r.text

        # 1. DATA
        data_match = re.search(r'(\d{1,2})\s+(maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre|gennaio|febbraio|marzo|aprile)', html, re.IGNORECASE)
        if not data_match: return
        data_csv = f"{data_match.group(1).zfill(2)}-{data_match.group(2).lower()[:3]}"

        # 2. NUMERI (Classi da image_62.png)
        sestina = re.findall(r'class="ball">(\d{1,2})</li>', html)[:6]
        jolly = re.search(r'class="jolly">(\d{1,2})</li>', html)
        star = re.search(r'class="superstar">(\d{1,2})</li>', html)

        if len(sestina) == 6 and jolly and star:
            # Formattazione rigorosa: tutti con lo zero davanti (zfill 2)
            numeri_finali = [n.zfill(2) for n in sestina]
            j_val = jolly.group(1).zfill(2)
            s_val = star.group(1).zfill(2)
            
            # Stringa dati senza spazi: data;n1;n2;n3;n4;n5;n6;jolly;star
            corpo_estrazione = f"{data_csv};{';'.join(numeri_finali)};{j_val};{s_val}"

            # 3. LETTURA E SCRITTURA SENZA RIGHE VUOTE
            if not os.path.exists(file_path): return
            
            with open(file_path, 'r', encoding='utf-8') as f:
                # Legge solo righe che contengono testo, eliminando quelle vuote
                righe = [l.strip() for l in f.readlines() if l.strip()]
            
            # Trova l'ultimo indice numerico valido
            ultimo_indice = 0
            if righe:
                ultimo_indice = int(righe[-1].split(';')[0])
            
            nuovo_indice = ultimo_indice + 1
            # Formato finale richiesto: INDICE;DATA;N1... (senza spazi)
            riga_finale = f"{nuovo_indice};{corpo_estrazione}"
            
            # Scrittura: sovrascrive il file per garantire che non ci siano righe vuote in mezzo
            with open(file_path, 'w', encoding='utf-8') as f:
                for riga in righe:
                    f.write(riga + '\n')
                f.write(riga_finale) # Scrive sempre l'ultima estrazione trovata
            
            print(f"✅ REGISTRATA correttamente: {riga_finale}")

    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    update_csv()
