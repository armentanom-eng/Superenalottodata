import requests
import os
import re
import time

def update_csv():
    file_path = 'storico_completo.csv'
    url = "https://www.superenalotto.net/"
    headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15'}

    try:
        # Tentativi di connessione per evitare il timeout di image_51.png
        html = ""
        for _ in range(3):
            r = requests.get(url, headers=headers, timeout=25)
            if r.status_code == 200:
                html = r.text
                break
            time.sleep(5)

        if not html: return

        # 1. DATA (es. 12-mag) - come appare in image_57.png
        data_match = re.search(r'(\d{1,2})\s+(maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre|gennaio|febbraio|marzo|aprile)', html, re.IGNORECASE)
        if not data_match: return
        data_csv = f"{data_match.group(1).zfill(2)}-{data_match.group(2).lower()[:3]}"

        # 2. CATTURA MIRATA BASATA SU image_57.png
        # Cerchiamo i numeri della sestina (palline standard)
        sestina = re.findall(r'class="ball">(\d{1,2})</li>', html)[:6]
        # Cerchiamo il Jolly (pallina rossa)
        jolly_match = re.search(r'class="ball\s+jolly">(\d{1,2})</li>', html)
        # Cerchiamo la SuperStar (stella gialla)
        star_match = re.search(r'class="ball\s+superstar">(\d{1,2})</li>', html)

        if len(sestina) == 6 and jolly_match and star_match:
            j = jolly_match.group(1)
            s = star_match.group(1)
            
            # Formattazione corretta per image_49.png: data;n1;n2;n3;n4;n5;n6;jolly;star
            # Usiamo int() per assicurarci che siano numeri puliti senza zeri extra non voluti
            corpo_dati = f"{data_csv};{';'.join(sestina)};{j};{s}"

            # 3. GESTIONE FILE E INDICE (image_49.png)
            if not os.path.exists(file_path): return
            with open(file_path, 'r', encoding='utf-8') as f:
                righe = [line.strip() for line in f.readlines() if line.strip()]
                ultima_riga = righe[-1]

            if data_csv not in ultima_riga:
                # Estraiamo l'indice iniziale (es. 4280)
                ultimo_indice = int(ultima_riga.split()[0])
                nuovo_indice = ultimo_indice + 1
                
                # Risultato: INDICE [3 SPAZI] DATI
                riga_finale = f"{nuovo_indice}   {corpo_dati}"
                
                with open(file_path, 'a', encoding='utf-8') as f:
                    f.write('\n' + riga_finale)
                print(f"✅ AGGIORNATO CON SUCCESSO: {riga_finale}")
            else:
                print(f"I dati del {data_csv} sono già nel file.")
    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    update_csv()
