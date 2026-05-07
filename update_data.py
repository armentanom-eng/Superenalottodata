import requests
from bs4 import BeautifulSoup
import os
import re
from datetime import datetime

def update_csv():
   file_path = 'storico_completo.csv'
   anno_corrente = datetime.now().year

   # Prova prima l'anno attuale, se fallisce prova l'anno prima
   urls_da_provare = [
       f"https://www.franknet.altervista.org/superena/{anno_corrente}.HTM",
       f"https://www.franknet.altervista.org/superena/{anno_corrente - 1}.HTM"
   ]

   headers = {
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
   }

   last_site_row = ""

   for url in urls_da_provare:
       try:
           print(f"Tentativo di lettura da: {url}")
           response = requests.get(url, headers=headers, timeout=20)
           if response.status_code != 200:
               continue

           response.encoding = 'utf-8'
           soup = BeautifulSoup(response.text, 'html.parser')
           rows = soup.find_all(re.compile(r'tr', re.I))

           for row in reversed(rows):
               cols = row.find_all(re.compile(r'td', re.I))
               if len(cols) >= 9:
                   dati_riga = [c.get_text(strip=True) for c in cols]
                   data_raw = dati_riga[0]

                   if len(data_raw) < 2 or "Data" in data_raw or not any(char.isdigit() for char in data_raw):
                       continue

                   data_sito = data_raw.replace(" ", "-")
                   numeri = dati_riga[1:7]
                   jolly = dati_riga[7]
                   superstar = dati_riga[8]

                   last_site_row = f"{data_sito};{';'.join(numeri)};{jolly};{superstar}"
                   break

           if last_site_row:
               break # Se abbiamo trovato i dati, usciamo dal ciclo degli URL

       except Exception as e:
           print(f"Errore su {url}: {e}")

   if not last_site_row:
       print("LOG: Impossibile trovare estrazioni valide negli URL provati.")
       return

   # Confronto e salvataggio
   try:
       if os.path.exists(file_path):
           with open(file_path, 'r', encoding='utf-8') as f:
               linee = [l.strip() for l in f.readlines() if l.strip()]
               ultima_riga_file = linee[-1] if linee else ""
       else:
           ultima_riga_file = ""

       print(f"SITO: {last_site_row}")
       print(f"FILE: {ultima_riga_file}")

       if last_site_row != ultima_riga_file:
           with open(file_path, 'a', encoding='utf-8') as f:
               f.write('\n' + last_site_row)
           print("ESITO: Nuovo concorso salvato!")
       else:
           print("ESITO: Già aggiornato.")
   except Exception as e:
       print(f"Errore file: {e}")

if __name__ == "__main__":
   update_csv()
