import requests
import os
import re
from datetime import datetime

def update_csv():
    file_path = 'storico_completo.csv'
    url = "https://www.adm.gov.it/portale/monopoli/giochi/giochi_num_total/superenalotto"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        r = requests.get(url, headers=headers, timeout=30)
        r.encoding = 'utf-8'
        testo = r.text

        # 1. CERCHIAMO LA DATA (es. 12/05/2026)
        data_match = re.search(r'(\d{2})/(\d{2})/(\d{4})', testo)
        if not data_match:
            print("❌ Data non trovata nella pagina.")
            return
        
        giorno, mese, anno = data_match.groups()
        mesi_ita = {"01":"gen","02":"feb","03":"mar","04":"apr","05":"mag","06":"giu","07":"lug","08":"ago","09":"set","10":"ott","11":"nov","12":"dic"}
        data_csv = f"{giorno}-{mesi_ita[mese]}"

        # 2. CERCHIAMO LA SESTINA (I 6 numeri dopo "Combinazione Vincente")
        # Puliamo i tag HTML per leggere solo i numeri
        testo_pulito = re.sub(r'<[^>]+>', ' ', testo)
        testo_pulito = ' '.join(testo_pulito.split())
        
        # Cerchiamo la combinazione vincente (6 numeri separati da spazi)
        search_comb = re.search(r'Combinazione Vincente\s+([\d\s]{11,20})\s+Numero Jolly', testo_pulito)
        if not search_comb:
            print("❌ Combinazione non trovata.")
            return
        
        sestina = search_comb.group(1).strip().replace(" ", ";")
        
        # 3. CERCHIAMO IL JOLLY
        search_jolly = re.search(r'Numero Jolly\s+(\d{1,2})', testo_pulito)
        jolly = search_jolly.group(1) if search_jolly else "0"

        # Superstar (Default a 0 se non lo troviamo subito, per non bloccare tutto)
        superstar = "0"
        search_super = re.search(r'SuperStar\s+(\d{1,2})', testo_pulito)
        if search_super: superstar = search_super.group(1)

        # 4. COSTRUIAMO LA RIGA DATI (CON IL PUNTO E VIRGOLA)
        nuova_estrazione_dati = f"{data_csv};{sestina};{jolly};{superstar}"

        # 5. LEGGIAMO IL CSV PER IL NUMERO PROGRESSIVO
        nuovo_indice = 1
        ultima_estrazione_csv = ""
        
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                righe = [l.strip() for l in f.readlines() if l.strip()]
                if righe:
                    ultima_riga_piena = righe[-1]
                    parti = ultima_riga_piena.split(';')
                    try:
                        nuovo_indice = int(parti[-1]) + 1
                        ultima_estrazione_csv = ";".join(parti[:-1])
                    except:
                        ultima_estrazione_csv = ultima_riga_piena

        # CONFRONTO E SCRITTURA
        print(f"DEBUG -> Sito: {nuova_estrazione_dati}")
        print(f"DEBUG -> CSV : {ultima_estrazione_csv}")

        if nuova_estrazione_dati != ultima_estrazione_csv:
            riga_finale = f"{nuova_estrazione_dati};{nuovo_indice}"
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write('\n' + riga_finale)
            print(f"✅ AGGIORNATO: Inserita estrazione n. {nuovo_indice} del {data_csv}")
        else:
            print("ℹ️ Il file è già aggiornato all'ultima estrazione ADM.")

    except Exception as e:
        print(f"⚠️ Errore tecnico: {e}")

if __name__ == "__main__":
    update_csv()
