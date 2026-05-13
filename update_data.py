import requests
import os
import re
from datetime import datetime

def update_csv():
    file_path = 'storico_completo.csv'
    # superenalotto.net è molto stabile e facile da leggere
    url = "https://www.superenalotto.net/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        r = requests.get(url, headers=headers, timeout=20)
        r.encoding = 'utf-8'
        html = r.text

        # 1. Trova la DATA (es. Martedì 12 Maggio 2026)
        # Cerchiamo il testo nel formato del sito
        data_match = re.search(r'(\d{1,2})\s+(Gennaio|Febbraio|Marzo|Aprile|Maggio|Giugno|Luglio|Agosto|Settembre|Ottobre|Novembre|Dicembre)\s+(\d{4})', html, re.IGNORECASE)
        if not data_match:
            print("Data non trovata.")
            return
        
        gg = data_match.group(1).zfill(2)
        mese_nome = data_match.group(2).lower()[:3] # Prende le prime 3 lettere (mag, giu...)
        data_csv = f"{gg}-{mese_nome}"

        # 2. Trova i NUMERI
        # Su superenalotto.net i numeri della sestina sono spesso dentro dei cerchietti (li prendiamo tutti)
        numeri = re.findall(r'<li class="ball">(\d{1,2})</li>', html)
        
        # Jolly e Superstar hanno classi diverse
        jolly_match = re.search(r'<li class="ball jolly">(\d{1,2})</li>', html)
        star_match = re.search(r'<li class="ball superstar">(\d{1,2})</li>', html)

        if len(numeri) < 6:
            print("Sestina non trovata.")
            return

        sestina = ";".join([n.zfill(2) for n in numeri[:6]])
        jolly = jolly_match.group(1).zfill(2) if jolly_match else "00"
        superstar = star_match.group(1).zfill(2) if star_match else "00"

        nuova_estrazione_dati = f"{data_csv};{sestina};{jolly};{superstar}"

        # 3. Gestione CSV e Indice Progressivo
        if not os.path.exists(file_path): return

        with open(file_path, 'r', encoding='utf-8') as f:
            righe = [l.strip() for l in f.readlines() if l.strip()]
            ultima_riga = righe[-1]

        # Confronto: se la data non c'è, aggiungiamo
        if data_csv not in ultima_riga:
            try:
                ultimo_indice = int(ultima_riga.split(';')[-1])
                nuovo_indice = ultimo_indice + 1
            except:
                nuovo_indice = 1
            
            riga_finale = f"{nuova_estrazione_dati};{nuovo_indice}"
            
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write('\n' + riga_finale)
            print(f"✅ AGGIORNATO DA SUPERENALOTTO.NET: {riga_finale}")
        else:
            print(f"Estrazione {data_csv} già presente.")

    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    update_csv()
