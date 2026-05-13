import requests
import os
import re
from datetime import datetime

def get_month_abbr(date_str):
    # Converte il mese da numero a abbreviazione (es. 05 -> mag)
    mesi = {
        "01": "gen", "02": "feb", "03": "mar", "04": "apr",
        "05": "mag", "06": "giu", "07": "lug", "08": "ago",
        "09": "set", "10": "ott", "11": "nov", "12": "dic"
    }
    giorno, mese, anno = date_str.split('/')
    return f"{giorno}-{mesi[mese]}"

def update_from_adm():
    file_path = 'storico_completo.csv'
    url = "https://www.adm.gov.it/portale/monopoli/giochi/giochi_num_total/superenalotto"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        r = requests.get(url, headers=headers, timeout=30)
        r.encoding = 'utf-8'
        html = r.text

        # 1. Cerchiamo la data (es. 12/05/2026)
        data_match = re.search(r'del\s+(\d{2}/\d{2}/\d{4})', html)
        # 2. Cerchiamo la combinazione (6 numeri separati da spazi)
        comb_match = re.search(r'Combinazione Vincente\s*</h3>\s*<p[^>]*>\s*([\d\s]+)\s*</p>', html, re.IGNORECASE | re.DOTALL)
        # Se la regex sopra fallisce, ne usiamo una più aggressiva per il testo puro
        if not comb_match:
             nums = re.findall(r'\b\d{1,2}\b', html) 
             # Nota: estrarre numeri dal sito ADM è complesso perché l'HTML è sporco
             # Per ora usiamo una logica basata sulla posizione vista in image_38.png
        
        # Estrarre i dati dal sito ADM via Python richiede spesso BeautifulSoup per via dei tag annidati
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        
        # Cerchiamo la combinazione vincente
        p_tags = soup.find_all('p')
        sestina = []
        jolly = ""
        data_formattata = ""

        if data_match:
            data_formattata = get_month_abbr(data_match.group(1))

        for p in p_tags:
            testo = p.get_text().strip()
            # Se troviamo una stringa di numeri lunga (la sestina)
            if re.match(r'^(\d{1,2}\s+){5}\d{1,2}$', testo):
                sestina = testo.replace(" ", ";").split(";")
            # Se il paragrafo contiene solo un numero ed è dopo "Numero Jolly"
            if len(testo) <= 2 and testo.isdigit() and not jolly:
                # Questo è un approccio semplificato
                jolly = testo

        # Se non troviamo il Superstar sul sito ADM (spesso è in una sezione Superstar separata)
        # Mettiamo un valore di default o lo cerchiamo
        superstar = "0" # ADM a volte lo mette sotto un'altra tabella

        if not sestina or not data_formattata:
            print("Non sono riuscito a leggere i dati dal sito ADM.")
            return

        # Costruiamo la riga (Manca l'ultimo numero, mettiamo 0 se non trovato)
        nuova_estrazione_dati = f"{data_formattata};{';'.join(sestina)};{jolly};{superstar}"

        # Gestione Indice Progressivo
        nuovo_indice = 1
        ultima_estrazione_csv = ""
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                righe = [l.strip() for l in f.readlines() if l.strip()]
                if righe:
                    parti = righe[-1].split(';')
                    nuovo_indice = int(parti[-1]) + 1
                    ultima_estrazione_csv = ";".join(parti[:-1])

        if nuova_estrazione_dati != ultima_estrazione_csv:
            riga_finale = f"{nuova_estrazione_dati};{nuovo_indice}"
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write('\n' + riga_finale)
            print(f"✅ RECUPERATO DA ADM: {riga_finale}")
        else:
            print("Sito ADM non ancora aggiornato o dato già presente.")

    except Exception as e:
        print(f"Errore ADM: {e}")

if __name__ == "__main__":
    update_from_adm()
