import requests
import os
import re
from datetime import datetime

def update_csv():
    file_path = 'storico_completo.csv'
    anno = datetime.now().year
    url = f"https://www.franknet.altervista.org/superena/{anno}.HTM"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        r = requests.get(url, headers=headers, timeout=20)
        r.encoding = 'utf-8'
        
        # Pulizia testo
        testo_puro = re.sub(r'<[^>]+>', ' ', r.text)
        testo_puro = ' '.join(testo_puro.split())

        # Cerchiamo tutte le estrazioni
        pattern = r'(\d{2}[-\s][a-zA-Z]{3})\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)'
        matches = re.findall(pattern, testo_puro)

        if not matches:
            print("ERRORE: Non trovo nessuna estrazione nella pagina!")
            return

        # STAMPA DI DEBUG: Vediamo le ultime 3 estrazioni che il bot ha trovato sul sito
        print(f"DEBUG - Ultime estrazioni trovate sul sito:")
        for m in matches[-3:]:
            print(f" -> {m[0]}")

        # Prendiamo l'ULTIMA assoluta
        m = matches[-1]
        data_sito = m[0].replace(" ", "-").lower()
        riga_sito = f"{data_sito};{m[1]};{m[2]};{m[3]};{m[4]};{m[5]};{m[6]};{m[7]};{m[8]}"

        # Leggiamo l'ultima del CSV
        ultima_csv = ""
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                righe = [l.strip() for l in f.readlines() if l.strip()]
                if righe: ultima_csv = righe[-1]

        print(f"CONFRONTO:\nSito: {riga_sito}\nCSV : {ultima_csv}")

        if riga_sito != ultima_csv:
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write('\n' + riga_sito)
            print(f"✅ AGGIORNATO: Inserito {data_sito}")
        else:
            print("❌ SALTATO: Il dato è già presente o lo script vede ancora il vecchio.")

    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    update_csv()
