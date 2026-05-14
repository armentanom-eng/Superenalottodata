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

        # Estrazione dati (struttura verificata da image_62.png)
        data_match = re.search(r'(\d{1,2})\s+(maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre|gennaio|febbraio|marzo|aprile)', html, re.IGNORECASE)
        if not data_match: return
        data_csv = f"{data_match.group(1).zfill(2)}-{data_match.group(2).lower()[:3]}"

        sestina = re.findall(r'class="ball">(\d{1,2})</li>', html)[:6]
        jolly = re.search(r'class="jolly">(\d{1,2})</li>', html)
        star = re.search(r'class="superstar">(\d{1,2})</li>', html)

        if len(sestina) == 6 and jolly and star:
            # Prepariamo la riga in formato INDICE;DATA;N1;N2;N3;N4;N5;N6;JOLLY;STAR
            n_finali = [n.zfill(2) for n in sestina]
            j_val = jolly.group(1).zfill(2)
            s_val = star.group(1).zfill(2)
            
            # Leggiamo SOLO l'ultima riga per calcolare il nuovo numero
            with open(file_path, 'r', encoding='utf-8') as f:
                righe = [l.strip() for l in f.readlines() if l.strip()]
            
            ultima_riga = righe[-1] if righe else "0;00-xxx;00;00;00;00;00;00;00;00"
            
            # Se l'estrazione non è già presente
            if data_csv not in ultima_riga:
                ultimo_indice = int(ultima_riga.split(';')[0])
                nuova_riga = f"{ultimo_indice + 1};{data_csv};{';'.join(n_finali)};{j_val};{s_val}"
                
                # 'a' significa APPEND: aggiunge solo alla fine, IMPOSSIBILE cancellare il sopra
                with open(file_path, 'a', encoding='utf-8') as f:
                    f.write('\n' + nuova_riga)
                print(f"Aggiunta riuscita: {nuova_riga}")
            else:
                print("Dati già aggiornati.")

    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    update_csv()
