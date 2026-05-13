import requests
import os
import re
from datetime import datetime

def update_csv():
    file_path = 'storico_completo.csv'
    url = "https://www.superenalotto.net/"
    headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15'}

    try:
        r = requests.get(url, headers=headers, timeout=20)
        r.encoding = 'utf-8'
        html = r.text

        # 1. DATA (es. 12-mag)
        data_match = re.search(r'(\d{1,2})\s+(maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre|gennaio|febbraio|marzo|aprile)', html, re.IGNORECASE)
        if not data_match: return
        data_csv = f"{data_match.group(1).zfill(2)}-{data_match.group(2).lower()[:3]}"

        # 2. NUMERI (Presi esattamente come appaiono in image_47.png)
        sestina = re.findall(r'<li class="ball">(\d{1,2})</li>', html)[:6]
        jolly_match = re.search(r'jolly">(\d{1,2})</li>', html)
        star_match = re.search(r'superstar">(\d{1,2})</li>', html)

        # Usiamo i numeri puliti, senza zeri aggiunti se non ci sono nel sito
        j = jolly_match.group(1) if jolly_match else "0"
        s = star_match.group(1) if star_match else "0"

        # 3. COSTRUZIONE RIGA (Format: data;n1;n2;n3;n4;n5;n6;jolly;star)
        corpo_dati = f"{data_csv};{';'.join(sestina)};{j};{s}"

        # 4. GESTIONE FILE
        if not os.path.exists(file_path): return
        with open(file_path, 'r', encoding='utf-8') as f:
            righe = [line.strip() for line in f.readlines() if line.strip()]
            ultima_riga = righe[-1]

        # Evitiamo duplicati
        if data_csv not in ultima_riga:
            # Estraiamo l'indice numerico iniziale (es. "4280")
            ultimo_indice = int(ultima_riga.split()[0])
            nuovo_indice = ultimo_indice + 1
            
            # Formato finale identico a image_49.png (Indice all'inizio, poi dati)
            # Usiamo 3 spazi per separare l'indice dalla data
            riga_finale = f"{nuovo_indice}   {corpo_dati}"
            
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write('\n' + riga_finale)
            print(f"✅ RIGA CORRETTA: {riga_finale}")

    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    update_csv()
