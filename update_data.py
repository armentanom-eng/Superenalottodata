import requests
from datetime import datetime

def fetch_data():
   try:
       # Sorgente dati affidabile
       url = "https://www.estrazionidellotto.it/api/estrazioni-superenalotto"
       headers = {'User-Agent': 'Mozilla/5.0'}
       response = requests.get(url, headers=headers, timeout=15)

       if response.status_code == 200:
           ultima = response.json()[0] 

           # FORMATTAZIONE DATA: da 2026-05-05 a 05-mag
           data_dt = datetime.strptime(ultima['data'], '%Y-%m-%d')
           mesi = ["gen", "feb", "mar", "apr", "mag", "giu", "lug", "ago", "set", "ott", "nov", "dic"]
           data_custom = f"{data_dt.day:02d}-{mesi[data_dt.month - 1]}"

           numeri = ultima['combinazione'] # I 6 numeri della sestina
           jolly = ultima['jolly']         # Il numero Jolly

           # Creiamo la riga: Data;N1;N2;N3;N4;N5;N6;Jolly
           # In totale 8 elementi separati da punto e virgola
           nuova_riga = f"{data_custom};{';'.join(map(str, numeri))};{jolly}"
           return nuova_riga
   except Exception as e:
       print(f"Errore durante il recupero: {e}")
   return None

def update_csv():
   file_path = 'storico_completo.csv'
   nuova_riga = fetch_data()

   if nuova_riga:
       with open(file_path, 'r') as f:
           lines = f.readlines()
           # Controlliamo se l'ultima riga del file ha già la stessa data
           if lines and nuova_riga.split(';')[0] in lines[-1]:
               print(f"L'estrazione del {nuova_riga.split(';')[0]} è già presente.")
               return

       # Aggiungiamo la riga in fondo al file
       with open(file_path, 'a') as f:
           f.write('\n' + nuova_riga)
       print(f"Successo! Aggiunta riga: {nuova_riga}")

if __name__ == "__main__":
   update_csv()
