import requests
from datetime import datetime

def fetch_data():
   try:
       # API ufficiale per recuperare l'ultimo concorso
       url = "https://www.superenalotto.it/api/risultati/ultima-estrazione"
       headers = {'User-Agent': 'Mozilla/5.0'}
       response = requests.get(url, headers=headers, timeout=15)

       if response.status_code == 200:
           json_data = response.json()
           # Estrazione dei dati
           data_raw = json_data['DataEstrazione'] # Es: "2026-05-05T00:00:00"
           data_dt = datetime.strptime(data_raw.split('T')[0], '%Y-%m-%d')
           data_formattata = data_dt.strftime('%d/%m/%Y')

           numeri = json_data['Combinazione'] # Lista di 6 numeri
           jolly = json_data['NumeroJolly']

           return f"{data_formattata};{';'.join(map(str, numeri))};{jolly}"
   except Exception as e:
       print(f"Errore: {e}")
   return None

def update_csv():
   file_path = 'storico_completo.csv'
   nuova_riga = fetch_data()

   if nuova_riga:
       with open(file_path, 'r') as f:
           content = f.read()

       if nuova_riga in content:
           print("Dati già presenti.")
       else:
           with open(file_path, 'a') as f:
               f.write('\n' + nuova_riga)
           print(f"Aggiunto: {nuova_riga}")

if __name__ == "__main__":
   update_csv()
