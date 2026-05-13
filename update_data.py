import requests
import os
import re
from datetime import datetime

def update_csv():
    file_path = 'storico_completo.csv'
    url = "https://www.superenalotto.net/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    try:
        r = requests.get(url, headers=headers, timeout=20)
        r.encoding = 'utf-8'
        html = r.text

        # 1. DATA: Martedì 12 maggio
        data_match = re.search(r'(\d{1,2})\s+(maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre|gennaio|febbraio|marzo|aprile)', html, re.IGNORECASE)
        if not data_match: return
        
        gg = data_match.group(1).zfill(2)
        mese_nome = data_match.group(2).lower()[:3]
        data_csv = f"{gg}-{mese_nome}"

        # 2. NUMERI: Estrazione mirata basata sulle classi HTML del sito in image_47.png
        # Sestina (palline verdi)
        sestina = re.findall(r'<li class="ball">(\d{1,2})</li>', html)[:6]
        # Jolly (pallina rossa)
        jolly_match = re.search(r'<li class="ball jolly">(\d{1,2})</li>', html)
        # SuperStar (stella gialla)
        star_match = re.search(r'<li class="ball superstar">(\d{1,2})</li>', html)

        j = jolly_match.group(1) if jolly_match else ""
        s = star_match.group(1) if star_match else ""

        # Componiamo la stringa dati: data;n1;n2;n3;n4;n5;n6;jolly;star
        # Usiamo i numeri così come sono (senza zfill(2)) per matchare il tuo storico
        stringa_numeri = ";".join(sestina)
        nuovi_dati = f"{data_csv};{stringa_numeri};{j};{s}"

        # 3. GESTIONE FILE E INDICE
        if not os.path.exists(file_path): return
        with open(file_path, 'r', encoding='utf-8') as f:
            righe = [line.strip() for line in f.readlines() if line.strip()]
            ultima_riga = righe[-1]

        # Se la data non è già presente nell'ultima riga
        if data_csv not in ultima_riga:
            # Estraiamo l'indice dall'inizio della riga (es. "4280")
            ultimo_indice = int(ultima_riga.split()[0])
            nuovo_indice = ultimo_indice + 1
            
            # Formato finale: INDICE [SPAZI] DATA;N1;N2;N3;N4;N5;N6;JOLLY;STAR
            # Ho aggiunto 3 spazi come sembra esserci nelle righe sopra la 4280
            nuova_riga = f"{nuovo_indice}   {nuovi_dati}"
            
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write('\n' + nuova_riga)
            print(f"✅ AGGIORNATO: {nuova_riga}")

    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    update_csv()
