import requests
import os
import re
import time
from datetime import datetime

def update_csv():
    file_path = 'storico_completo.csv'
    url = "https://www.superenalotto.net/"
    
    # Header super realistici per sembrare un iPhone (come quello che usi tu!)
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'it-it',
        'Connection': 'keep-alive'
    }

    try:
        # Aggiungiamo un piccolo delay per non sembrare un bot istantaneo
        time.sleep(2)
        
        response = requests.get(url, headers=headers, timeout=30)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            print(f"Il sito ha risposto con errore {response.status_code}")
            return

        html = response.text

        # 1. DATA: (Es: 12 maggio) - Basato su image_47.png
        data_match = re.search(r'(\d{1,2})\s+(maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre|gennaio|febbraio|marzo|aprile)', html, re.IGNORECASE)
        if not data_match:
            print("Non riesco a trovare la data nella pagina.")
            return
        
        gg = data_match.group(1).zfill(2)
        mese_nome = data_match.group(2).lower()[:3]
        data_csv = f"{gg}-{mese_nome}"

        # 2. NUMERI: Estrazione specifica (Sestina, Jolly, Star)
        sestina = re.findall(r'<li class="ball">(\d{1,2})</li>', html)[:6]
        jolly_match = re.search(r'jolly">(\d{1,2})</li>', html)
        star_match = re.search(r'superstar">(\d{1,2})</li>', html)

        j = jolly_match.group(1) if jolly_match else ""
        s = star_match.group(1) if star_match else ""

        if not sestina:
            print("Non ho trovato i numeri.")
            return

        # Componiamo i dati: data;n1;n2;n3;n4;n5;n6;jolly;star
        stringa_numeri = ";".join(sestina)
        nuovi_dati = f"{data_csv};{stringa_numbers};{j};{s}"

        # 3. GESTIONE FILE E INDICE (Formato image_46.png)
        if not os.path.exists(file_path): return
        with open(file_path, 'r', encoding='utf-8') as f:
            righe = [line.strip() for line in f.readlines() if line.strip()]
            ultima_riga = righe[-1]

        if data_csv not in ultima_riga:
            ultimo_indice = int(ultima_riga.split()[0])
            nuovo_indice = ultimo_indice + 1
            
            # Formato: INDICE [3 SPAZI] DATI
            nuova_riga = f"{nuovo_indice}   {nuovi_dati}"
            
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write('\n' + nuova_riga)
            print(f"✅ AGGIORNAMENTO RIUSCITO: {nuova_riga}")
        else:
            print(f"Estrazione del {data_csv} già presente.")

    except Exception as e:
        print(f"⚠️ Errore di connessione: {e}. Il sito ha bloccato GitHub.")

if __name__ == "__main__":
    update_csv()
