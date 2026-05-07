import requests
from bs4 import BeautifulSoup
from datetime import datetime

def update_csv():
   file_path = 'storico_completo.csv'

   # 1. Recuperiamo l'anno corrente
   anno_corrente = datetime.now().year

   # 2. Costruiamo il link con l'estensione .HTM come mi hai indicato
   # Esempio: https://www.franknet.altervista.org/superena/2026.HTM
   url = f"https://www.franknet.altervista.org/superena/{anno_corrente}.HTM"

   headers = {
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
   }

   try:
       response = requests.get(url, headers=headers, timeout=20)

       # Se il sito risponde (200 OK)
       if response.status_code == 200:
           soup = BeautifulSoup(response.text, 'html.parser')
           rows = soup.find_all('tr')

           ultima_estrazione = ""

           # 3. Cerchiamo l'ultima riga valida (partendo dal fondo della tabella)
           for row in reversed(rows):
               cols = row.find_all('td')
               if len(cols) >= 8:
                   testo_data = cols[0].text.strip()
                   # Verifichiamo che sia una riga con una data (es. contiene un mese)
                   mesi = ["gen", "feb", "mar", "apr", "mag", "giu", "lug", "ago", "set", "ott", "nov", "dic"]
                   if any(m in testo_data.lower() for m in mesi):
                       # Trasformiamo "05 mag" in "05-mag" per la tua app
                       data_per_app = testo_data.replace(" ", "-")

                       # Prendiamo i 6 numeri e il Jolly
                       numeri = [cols[i].text.strip() for i in range(1, 7)]
                       jolly = cols[7].text.strip()

                       ultima_estrazione = f"{data_per_app};{';'.join(numeri)};{jolly}"
                       break

           if ultima_estrazione:
               # 4. Leggiamo il file CSV attuale
               with open(file_path, 'r') as f:
                   content = f.read()

               # Se la data non c'è già, aggiungiamo la riga
               if ultima_estrazione.split(';')[0] not in content:
                   with open(file_path, 'a') as f:
                       # Assicuriamoci che inizi su una nuova riga
                       if content and not content.endswith('\n'):
                           f.write('\n')
                       f.write(ultima_estrazione)
                   print(f"AGGIORNAMENTO RIUSCITO: {ultima_estrazione}")
               else:
                   print(f"L'estrazione {ultima_estrazione.split(';')[0]} è già presente.")
       else:
           print(f"Errore: Il link {url} ha restituito codice {response.status_code}")

   except Exception as e:
       print(f"Errore tecnico: {e}")

if __name__ == "__main__":
   update_csv()
