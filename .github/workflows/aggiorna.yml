import requests
from bs4 import BeautifulSoup
import os

def update_csv():
   file_path = 'storico_completo.csv'
   # URL di FrankNet (molto semplice da scansionare)
   url = "https://www.franknet.altervista.org/superena/2026.HTM"
   headers = {'User-Agent': 'Mozilla/5.0'}

   try:
       response = requests.get(url, headers=headers, timeout=20)
       response.encoding = 'utf-8'
       soup = BeautifulSoup(response.text, 'html.parser')
       rows = soup.find_all('tr')

       # 1. Prendiamo l'ULTIMA riga dal sito
       for row in reversed(rows):
           cols = row.find_all('td')
           if len(cols) >= 9:
               data_sito = cols[0].text.strip().replace(" ", "-")
               numeri = [cols[i].text.strip() for i in range(1, 7)]
               jolly = cols[7].text.strip()
               superstar = cols[8].text.strip()
               nuova_estrazione = f"{data_sito};{';'.join(numeri)};{jolly};{superstar}"
               break

       # 2. Leggiamo l'ULTIMA riga del tuo file
       if os.path.exists(file_path):
           with open(file_path, 'r') as f:
               linee = [l.strip() for l in f.readlines() if l.strip()]
               ultima_riga_file = linee[-1] if linee else ""
       else:
           ultima_riga_file = ""

       # 3. CONFRONTO DIRETTO: Aggiunge solo se l'ultima riga è diversa
       if nuova_estrazione != ultima_riga_file:
           with open(file_path, 'a') as f:
               f.write('\n' + nuova_estrazione)
           print(f"AGGIORNATO: {nuova_estrazione}")
       else:
           print("Nessuna nuova estrazione rispetto all'ultima salvata.")

   except Exception as e:
       print(f"Errore: {e}")

if __name__ == "__main__":
   update_csv()
