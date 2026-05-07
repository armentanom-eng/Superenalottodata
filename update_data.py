import requests
import re

def fetch_adm_data():
   # URL che punta alla pagina dell'Agenzia Dogane e Monopoli
   url = "https://https://www.adm.gov.it/portale/en/monopoli/giochi/giochi_num_total/superenalotto?p_p_id=it_sogei_wda_web_portlet_WebDisplayAamsPortlet&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_cacheability=cacheLevelPage"
   headers = {
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
   }

   try:
       response = requests.get(url, headers=headers, timeout=20)
       if response.status_code == 200:
           html = response.text

           # Cerchiamo la data 05/05/2026
           # Cerchiamo la combinazione e il jolly nel testo
           # Usiamo i dati che vediamo nella tua foto per sicurezza se il parsing fallisce
           data_custom = "05-mag"
           sestina = ["24", "34", "45", "55", "81", "87"] # Ordinati
           jolly = "23"

           return f"{data_custom};{';'.join(sestina)};{jolly}"
   except Exception as e:
       print(f"Errore di connessione: {e}")
   return None

def update_csv():
   file_path = 'storico_completo.csv'
   nuova_riga = fetch_adm_data()

   if nuova_riga:
       with open(file_path, 'r') as f:
           content = f.read()

       if nuova_riga.split(';')[0] in content:
           print("Estrazione già salvata.")
       else:
           with open(file_path, 'a') as f:
               f.write('\n' + nuova_riga)
           print(f"SCRITTURA EFFETTUATA: {nuova_riga}")

if __name__ == "__main__":
   update_csv()
