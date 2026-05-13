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
        print(f"Verifica link: {url}")
        r = requests.get(url, headers=headers, timeout=20)
        r.encoding = 'utf-8'

        if r.status_code != 200:
            print(f"Errore connessione: {r.status_code}")
            return

        # 1. Pulizia testo per rendere i dati leggibili dalla Regex
        testo_puro = re.sub(r'<[^>]+>', ' ', r.text)
        testo_puro = ' '.join(testo_puro.split())

        # 2. Regex per trovare tutte le righe (Data + 8 numeri)
        pattern = r'(\d{2}[-\s][a-zA-Z]{3})\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)'
        matches = re.findall(pattern, testo_puro)

        if not matches:
            print("Nessun dato trovato nella pagina.")
            return

        # 3. IDENTIFICHIAMO L'ULTIMA RIGA DEL SITO (Quella che dovrebbe essere il 12-mag)
        m = matches[-1] 
        data_sito = m[0].replace(" ", "-").lower()
        riga_sito = f"{data_sito};{m[1]};{m[2]};{m[3]};{m[4]};{m[5]};{m[6]};{m[7]};{m[8]}"
        
        print(f"ULTIMO DATO SUL SITO: {riga_sito}")

        # 4. LEGGIAMO L'ULTIMA RIGA DEL TUO FILE CSV
        ultima_csv = ""
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                righe = [l.strip() for l in f.readlines() if l.strip()]
                if righe:
                    ultima_csv = righe[-1]

        # 5. IL CONFRONTO: Se l'ultima del sito è diversa dall'ultima del CSV, scriviamo
        if riga_sito != ultima_csv:
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write('\n' + riga_sito)
            print(f"SUCCESSO: Aggiunta l'estrazione del {data_sito}!")
        else:
            print(f"SISTEMA AGGIORNATO: L'estrazione del {data_sito} è già presente.")

    except Exception as e:
        print(f"Errore durante l'esecuzione: {e}")

if __name__ == "__main__":
    update_csv()
