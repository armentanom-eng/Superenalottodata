import requests
from datetime import datetime

def fetch_data():
   # Questo è il link "motore" di Sisal, molto più stabile della pagina web
   url = "https://www.superenalotto.it/api-m/estrazioni/ultima"
   headers = {
       'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
   }

   try:
       response = requests.get(url, headers=headers, timeout=20)
       if response.status_code == 200:
           data_json = response.json()
           estrazione = data_json['estrazione']

           # TRASFORMAZIONE DATA: da 20260505 a 05-mag
           data_raw = estrazione['dataEstrazione'] # "20260505"
           dt = datetime.strptime(data_raw, '%Y%m%d')
           mesi = ["gen", "feb", "mar", "apr", "mag", "giu", "lug", "ago", "set", "ott", "nov", "dic"]
           data_custom = f"{dt.day:02d}-{mesi[dt.month - 1]}"

           # PRENDIAMO I NUMERI (proprio quelli della tua foto!)
           combinazione = estrazione['combinazione'] # [24, 34, 45, 55, 81, 87]
           jolly = estrazione['jolly']               # 23

           return f"{data_custom};{';'.join(map(str, combinazione))};{jolly}"
   except Exception as e:
       print(f"Errore: {e}")
   return None

def update_csv():
   file_path = 'storico_completo.csv'
   nuova_riga = fetch_data()

   if nuova_riga:
       with open(file_path, 'r') as f:
           content = f.read()

       if nuova_riga.split(';')[0] in content:
           print("Estrazione già presente.")
       else:
           with open(file_path, 'a') as f:
               f.write('\n' + nuova_riga)
           print(f"Successo! Aggiunta riga: {nuova_riga}")

if __name__ == "__main__":
   update_csv()
