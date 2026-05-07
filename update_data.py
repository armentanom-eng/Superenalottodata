import requests
import re
from datetime import datetime

def fetch_data():
   # Sito di notizie ufficiale sui giochi, molto stabile e senza blocchi 404
   url = "https://www.agipronews.it/flash-news/superenalotto-estrazione-ultima"
   headers = {'User-Agent': 'Mozilla/5.0'}

   try:
       response = requests.get(url, headers=headers, timeout=20)
       if response.status_code == 200:
           testo = response.text

           # 1. Cerchiamo la sestina (cerca gruppi di numeri separati da spazi o trattini)
           # Cerchiamo la combinazione vincente nel testo
           numeri = re.findall(r'\b([1-9]|[1-8][0-9]|90)\b', testo)

           # Di solito i primi 6 sono la combinazione, il 7° è il Jolly
           if len(numeri) >= 7:
               sestina = numeri[0:6]
               jolly = numeri[6]

               # 2. Gestione Data: prendiamo la data di oggi nel tuo formato
               dt = datetime.now()
               mesi = ["gen", "feb", "mar", "apr", "mag", "giu", "lug", "ago", "set", "ott", "nov", "dic"]
               data_custom = f"{dt.day:02d}-{mesi[dt.month - 1]}"

               return f"{data_custom};{';'.join(sestina)};{jolly}"
   except Exception as e:
       print(f"Errore durante il recupero: {e}")
   return None

def update_csv():
   file_path = 'storico_completo.csv'
   nuova_riga = fetch_data()

   if nuova_riga:
       with open(file_path, 'r') as f:
           content = f.read()

       # Se la data non c'è, scriviamo
       if nuova_riga.split(';')[0] not in content:
           with open(file_path, 'a') as f:
               f.write('\n' + nuova_riga)
           print(f"Aggiornato con successo: {nuova_riga}")
       else:
           print("Estrazione già presente.")

if __name__ == "__main__":
   update_csv()

Inviato da iPhone
