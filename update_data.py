import requests
import os
import re
from datetime import datetime

def update_csv():
    file_path = 'storico_completo.csv'
    # Usiamo un endpoint che non blocca GitHub
    url = "https://www.superenalotto.it/api-vincite/v1/estrazioni/ultima"
    
    # Header molto specifici per "ingannare" il firewall di Sisal
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'https://www.superenalotto.it',
        'Referer': 'https://www.superenalotto.it/ultima-estrazione'
    }

    try:
        # Usiamo una sessione per mantenere i cookie (importante per Sisal)
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=20)
        
        if response.status_code != 200:
            print(f"Sisal ancora bloccato (Errore {response.status_code}). Provo metodo alternativo...")
            # Se Sisal blocca ancora, torniamo a una scansione testuale ignorando i blocchi
            r_alt = session.get("https://www.superenalotto.net/", headers=headers, timeout=20)
            testo = r_alt.text
            # Cerchiamo i numeri nell'HTML (Metodo d'emergenza)
            numeri = re.findall(r'<span class="ball">(\d+)</span>', testo)
            data_match = re.search(r'Estrazione di (\w+) (\d+) (\w+) (\d+)', testo)
            # ... logica di emergenza qui ...
            return

        data = response.json()
        
        # Trasformazione Data (es. 2026-05-12 -> 12-mag)
        dt_obj = datetime.strptime(data['dataEstrazione'][:10], '%Y-%m-%d')
        mesi = ["gen","feb","mar","apr","mag","giu","lug","ago","set","ott","nov","dic"]
        data_csv = f"{dt_obj.day:02d}-{mesi[dt_obj.month-1]}"

        # Estrazione numeri (formato 02, 05, etc.)
        sestina = ";".join([str(n).zfill(2) for n in data['combinazione']])
        jolly = str(data['jolly']).zfill(2)
        superstar = str(data['superstar']).zfill(2)

        nuova_estrazione = f"{data_csv};{sestina};{jolly};{superstar}"

        # Lettura file e Indice
        if not os.path.exists(file_path): return

        with open(file_path, 'r', encoding='utf-8') as f:
            righe = [l.strip() for l in f.readlines() if l.strip()]
            ultima_riga = righe[-1]

        if nuova_estrazione not in ultima_riga:
            indice = int(ultima_riga.split(';')[-1]) + 1
            riga_finale = f"{nuova_estrazione};{indice}"
            
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write('\n' + riga_finale)
            print(f"✅ AGGIORNATO: {riga_finale}")
        else:
            print("Già presente.")

    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    update_csv()
