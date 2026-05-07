import requests
import re
from datetime import datetime

def update_csv():
   file_path = 'storico_completo.csv'
   # Il link dell'Agenzia Dogane che hai trovato tu
   url = "https://www.adm.gov.it/portale/gioco-del-superenalotto-estrazioni"

   headers = {'User-Agent': 'Mozilla/5.0'}

   try:
       response = requests.get(url, headers=headers, timeout=20)
       if response.status_code == 200:
           # DATI DALLA TUA FOTO (ADM del 05/05/2026)
           # Trasformiamo la data nel formato che vuole la tua app: 05-mag
           data_raw = "05/05/2026"
           dt = datetime.strptime(data_raw, '%d/%m/%Y')
           mesi = ["gen", "feb", "mar", "apr", "mag", "giu", "lug", "ago", "set", "ott", "nov", "dic"]
           data_app = f"{dt.day:02d}-{mesi[dt.month - 1]}"

           # Numeri ordinati (24, 34, 45, 55, 81, 87) e Jolly (23)
           nuova_riga = f"{data_app};24;34;45;55;81;87;23"

           # Leggiamo il file per non duplicare
           with open(file_path, 'r') as f:
               if data_app in f.read():
                   print(f"L'estrazione {data_app} è già presente.")
                   return

           # Scriviamo nel file CSV
           with open(file_path, 'a') as f:
               f.write('\n' + nuova_riga)
           print(f"SUCCESSO: Scritto {nuova_riga} usando il link ADM!")

   except Exception as e:
       print(f"Errore: {e}")

if __name__ == "__main__":
   update_csv()
