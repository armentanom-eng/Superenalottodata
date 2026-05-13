Import requests
import os
import re
from datetime import datetime

def update_csv():
   file_path = 'storico_completo.csv'
   anno = datetime.now().year

   # Proviamo gli URL che hai confermato funzionanti
   urls = [
       f"https://www.franknet.altervista.org/superena/{anno}.HTM",
       f"https://www.franknet.altervista.org/superena/{anno-1}.HTM"
   ]

   headers = {
       'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Language': 'it-it'
   }

   last_site_row = ""

   for url in urls:
       try:
           print(f"Verifica link: {url}")
           r = requests.get(url, headers=headers, timeout=20)
           r.encoding = 'utf-8'

           if r.status_code != 200:
               print(f"Link non raggiungibile (Errore {r.status_code})")
               continue

           # 1. Pulizia totale dai tag HTML per evitare interferenze
           testo_puro = re.sub(r'<[^>]+>', ' ', r.text)
           testo_puro = ' '.join(testo_puro.split())

           # 2. Regex ultra-flessibile: 
           # Cerca una data (es. 05-mag o 05 mag) seguita da 8 gruppi di numeri
           pattern = r'(\d{2}[-\s][a-zA-Z]{3})\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)'
           matches = re.findall(pattern, testo_puro)

           if matches:
               # Prendiamo l'ultima estrazione trovata nella pagina
               m = matches[-1]
               data_finale = m[0].replace(" ", "-").lower()
               last_site_row = f"{data_finale};{m[1]};{m[2]};{m[3]};{m[4]};{m[5]};{m[6]};{m[7]};{m[8]}"
               print(f"DATI TROVATI: {last_site_row}")
               break
           else:
               print("Dati non trovati nel testo della pagina. Controllo struttura...")
               # Stampiamo i primi 200 caratteri per capire cosa vede lo script
               print(f"Anteprima testo: {testo_puro[:200]}")

       except Exception as e:
           print(f"Errore tecnico: {e}")

   if not last_site_row:
       return

   # Confronto con il file CSV locale
   ultima_file = ""
   if os.path.exists(file_path):
       with open(file_path, 'r', encoding='utf-8') as f:
           righe = [l.strip() for l in f.readlines() if l.strip()]
           if righe: ultima_file = righe[-1]

   if last_site_row != ultima_file:
       with open(file_path, 'a', encoding='utf-8') as f:
           f.write('\n' + last_site_row)
       print("COMPLETATO: Nuovi dati aggiunti al CSV!")
   else:
       print("OK: Il file è già aggiornato all'ultima estrazione.")

if __name__ == "__main__":
update_csv()
