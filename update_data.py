import requests
import os
from datetime import datetime

def update_csv():
    file_path = 'storico_completo.csv'
    # URL dell'API ufficiale che alimenta la pagina di image_41.png
    url = "https://www.superenalotto.it/api-vincite/v1/estrazioni/ultima"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json'
    }

    try:
        response = requests.get(url, headers=headers, timeout=20)
        if response.status_code != 200:
            print(f"Errore connessione Sisal: {response.status_code}")
            return

        data_json = response.json()
        
        # Estrazione dati dall'API (corrispondenti a image_41.png)
        # Data: da "2026-05-12T20:00:00" a "12-mag"
        dt = datetime.strptime(data_json['dataEstrazione'][:10], '%Y-%m-%d')
        mesi = ["gen","feb","mar","apr","mag","giu","lug","ago","set","ott","nov","dic"]
        data_formattata = f"{dt.day:02d}-{mesi[dt.month-1]}"
        
        # Combinazione (Sestina)
        sestina = ";".join([str(n).zfill(2) for n in data_json['combinazione'])
        
        # Jolly e Superstar
        jolly = str(data_json['jolly']).zfill(2)
        superstar = str(data_json['superstar']).zfill(2)
        
        # Costruiamo la parte dati dell'estrazione
        nuovi_dati_estrazione = f"{data_formattata};{sestina};{jolly};{superstar}"

        # Gestione Indice Progressivo nel CSV
        if not os.path.exists(file_path):
            print("File CSV non trovato.")
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            righe = [l.strip() for l in f.readlines() if l.strip()]
            ultima_riga = righe[-1]
        
        # Se i dati dell'estrazione sono già nell'ultima riga, ci fermiamo
        if nuovi_dati_estrazione in ultima_riga:
            print(f"Dato del {data_formattata} già presente (Sisal).")
            return

        # Calcoliamo il nuovo indice (es. 4280 + 1)
        try:
            ultimo_indice = int(ultima_riga.split(';')[-1])
            nuovo_indice = ultimo_indice + 1
        except:
            nuovo_indice = 1

        # Riga finale con punto e virgola
        riga_finale = f"{nuovi_dati_estrazione};{nuovo_indice}"

        with open(file_path, 'a', encoding='utf-8') as f:
            f.write('\n' + riga_finale)
        
        print(f"✅ AGGIORNATO DA SISAL: {riga_finale}")

    except Exception as e:
        print(f"Errore tecnico API Sisal: {e}")

if __name__ == "__main__":
    update_csv()
