import requests
import os
import re

def update_csv():
    file_path = 'storico_completo.csv'
    # Agipro è molto più permissivo con gli script
    url = "https://www.agipronews.it/lotto-e-superenalotto/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.encoding = 'utf-8'
        html = response.text

        # 1. Estrazione Data (es. 12 maggio)
        data_match = re.search(r'(\d{1,2})\s+(gennaio|febbraio|marzo|aprile|maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre)', html, re.IGNORECASE)
        if not data_match:
            print("Data non trovata.")
            return
        
        gg = data_match.group(1).zfill(2)
        mese_it = data_match.group(2).lower()[:3]
        data_csv = f"{gg}-{mese_it}"

        # 2. Estrazione Numeri (Sestina, Jolly, Superstar)
        # Cerchiamo i numeri all'interno dei tag strong o classi specifiche del sito
        numeri = re.findall(r'<strong>(\d{1,2})</strong>', html)
        
        if len(numeri) < 8:
            # Fallback se la struttura è diversa
            numeri = re.findall(r'>(\d{1,2})<', html)

        if len(numeri) >= 8:
            sestina = ";".join(numeri[:6])
            jolly = numeri[6]
            star = numeri[7]
            
            nuovi_dati = f"{data_csv};{sestina};{jolly};{star}"

            # 3. Aggiornamento File
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    righe = [l.strip() for l in f.readlines() if l.strip()]
                
                ultima_riga = righe[-1]
                if data_csv not in ultima_riga:
                    ultimo_indice = int(ultima_riga.split()[0])
                    nuovo_indice = ultimo_indice + 1
                    
                    # Formato con 3 spazi: INDICE   DATI
                    riga_finale = f"{nuovo_indice}   {nuovi_dati}"
                    
                    with open(file_path, 'a', encoding='utf-8') as f:
                        f.write('\n' + riga_finale)
                    print(f"✅ AGGIORNATO: {riga_finale}")
                else:
                    print(f"Dati del {data_csv} già presenti.")
    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    update_csv()
