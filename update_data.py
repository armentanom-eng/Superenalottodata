import requests
import os
import re
from datetime import datetime

def update_csv():
    file_path = 'storico_completo.csv'
    # Estrazioni.org è molto stabile e bot-friendly
    url = "https://www.estrazioni.org/superenalotto/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        r = requests.get(url, headers=headers, timeout=20)
        r.encoding = 'utf-8'
        html = r.text

        # 1. Recupero della data (es. 12/05/2026)
        data_match = re.search(r'(\d{2})/(\d{2})/(\d{4})', html)
        if not data_match:
            print("Data non trovata.")
            return
        
        gg, mm, aaaa = data_match.groups()
        mesi_it = {"01":"gen","02":"feb","03":"mar","04":"apr","05":"mag","06":"giu","07":"lug","08":"ago","09":"set","10":"ott","11":"nov","12":"dic"}
        data_formattata = f"{gg}-{mesi_it[mm]}"

        # 2. Recupero dei numeri (sestina + jolly + superstar)
        # Cerchiamo i cerchietti dei numeri che solitamente hanno una classe specifica
        numeri = re.findall(r'<span class="ball(?:_jolly|_star)?">(\d{1,2})</span>', html)
        
        if len(numeri) < 8:
            # Secondo tentativo con una regex più generica se la classe cambia
            numeri = re.findall(r'>(\d{1,2})</span>', html)[:8]

        if len(numeri) < 7:
            print("Numeri non rilevati correttamente.")
            return

        # Formattazione: 6 numeri sestina + jolly + superstar (se presente)
        sestina = ";".join([n.zfill(2) for n in numeri[:6]])
        jolly = numeri[6].zfill(2)
        superstar = numeri[7].zfill(2) if len(numeri) >= 8 else "00"

        nuova_estrazione = f"{data_formattata};{sestina};{jolly};{superstar}"

        # 3. Confronto con il CSV locale
        if not os.path.exists(file_path): return
        
        with open(file_path, 'r', encoding='utf-8') as f:
            righe = [l.strip() for l in f.readlines() if l.strip()]
            ultima_riga = righe[-1]

        if data_formattata not in ultima_riga:
            # Calcolo nuovo indice progressivo
            nuovo_indice = int(ultima_riga.split(';')[-1]) + 1
            riga_finale = f"{nuova_estrazione};{nuovo_indice}"
            
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write('\n' + riga_finale)
            print(f"✅ AGGIORNATO DA ESTRAZIONI.ORG: {riga_finale}")
        else:
            print(f"L'estrazione del {data_formattata} è già presente.")

    except Exception as e:
        print(f"Errore durante il recupero: {e}")

if __name__ == "__main__":
    update_csv()
