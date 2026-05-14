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

        # 1. Recupero dati dal sito
        data_match = re.search(r'(\d{1,2})\s+(maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre|gennaio|febbraio|marzo|aprile)', html, re.IGNORECASE)
        if not data_match: return
        data_csv = f"{data_match.group(1).zfill(2)}-{data_match.group(2).lower()[:3]}"

        sestina = re.findall(r'class="ball">(\d{1,2})</li>', html)[:6]
        jolly = re.search(r'class="jolly">(\d{1,2})</li>', html)
        star = re.search(r'class="superstar">(\d{1,2})</li>', html)

        if len(sestina) == 6 and jolly and star:
            # Prepariamo la riga
            n_finali = [n.zfill(2) for n in sestina]
            corpo = f"{data_csv};{';'.join(n_finali)};{jolly.group(1).zfill(2)};{star.group(1).zfill(2)}"

            # 2. Leggiamo SOLO l'ultima riga per l'indice (senza toccare il resto)
            with open(file_path, 'r', encoding='utf-8') as f:
                righe = [l.strip() for l in f.readlines() if l.strip()]
            
            # Cerchiamo l'ultimo indice buono
            ultimo_indice = 0
            for riga in reversed(righe):
                parti = riga.split(';')
                if parti[0].isdigit():
                    ultimo_indice = int(parti[0])
                    break
            
            # 3. SCRITTURA IN APPEND (Aggiunge solo alla fine)
            if data_csv not in righe[-1]:
                nuovo_indice = ultimo_indice + 1
                riga_da_aggiungere = f"{nuovo_indice};{corpo}"
                
                with open(file_path, 'a', encoding='utf-8') as f:
                    f.write('\n' + riga_da_aggiungere)
                print(f"Aggiunta riga: {riga_da_aggiungere}")

    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    update_csv()
