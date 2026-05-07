import requests
from bs4 import BeautifulSoup
import os

def update_csv():
   file_path = 'storico_completo.csv'
   url = "https://www.franknet.altervista.org/superena/2026.HTM"
   headers = {'User-Agent': 'Mozilla/5.0'}

   try:
       response = requests.get(url, headers=headers, timeout=20)
       response.encoding = 'utf-8'
       soup = BeautifulSoup(response.text, 'html.parser')
       rows = soup.find_all('tr')

       last_site_row = ""
       # 1. Recupero l'ultima riga dal sito
       for row in reversed(rows):
           cols = row.find_all('td')
           if len(cols) >= 9:
               data_sito = cols[0].text.strip().replace(" ", "-")
               numeri = [cols[i].text.strip() for i in range(1, 7)]
               jolly = cols[7].text.strip()
               superstar = cols[8].text.strip()
               # Definiamo la variabile correttamente
               last_site_row = f"{data_sito};{';'.join(numeri)};{jolly};{superstar}"
               break

       if not last_site_row:
           print("Non ho trovato dati sul sito.")
           return

       # 2. Leggo l'ultima riga dal file
       if os.path.exists(file_path):
           with open(file_path, 'r') as f:
               linee = [l.strip() for l in f.readlines() if l.strip()]
               ultima_riga_file = linee[-1] if linee else ""
       else:
           ultima_riga_file = ""

       # 3. Confronto e aggiunta
       if last_site_row != ultima_riga_file:
           with open(file_path, 'a') as f:
               # Scriviamo la riga
               f.write('\n' + last_site_row)
           print(f"AGGIORNATO: {last_site_row}")
       else:
           print("Nessun nuovo aggiornamento necessario.")

   except Exception as e:
       print(f"Errore durante l'esecuzione: {e}")

if __name__ == "__main__":
   update_csv()
