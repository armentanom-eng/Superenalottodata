import requests
import os
import re
import time

def update_csv():
    file_path = 'storico_completo.csv'
    url = "https://www.superenalotto.net/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1'
    }

    html = ""
    for i in range(3): # Prova 3 volte per evitare il timeout di image_51.png
        try:
            r = requests.get(url, headers=headers, timeout=20)
            r.encoding = 'utf-8'
            if r.status_code == 200:
                html = r.text
                break
        except:
            time.sleep(5)
            continue

    if not html:
        print("Errore: Impossibile connettersi al sito dopo 3 tentativi.")
        return

    # 1. Estrazione DATA (Es: 12 maggio)
    data_match = re.search(r'(\d{1,2})\s+(maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre|gennaio|febbraio|marzo|aprile)', html, re.IGNORECASE)
    if not data_match:
        print("Data non trovata nel codice HTML.")
        return
    
    gg = data_match.group(1).zfill(2)
    mese = data_match.group(2).lower()[:3]
    data_csv = f"{gg}-{mese}"

    # 2. Estrazione NUMERI (Sestina, Jolly, Star) come da image_47.png
    sestina = re.findall(r'<li class="ball">(\d{1,2})</li>', html)[:6]
    jolly_match = re.search(r'ball jolly">(\d{1,2})</li>', html)
    star_match = re.search(r'ball superstar">(\d{1,2})</li>', html)

    if not sestina or not jolly_match or not star_match:
        print("Numeri non trovati correttamente.")
        return

    j = jolly_match.group(1)
    s = star_match.group(1)

    # 3. COSTRUZIONE RIGA (Correzione errore image_49.png)
    # Formato voluto: INDICE [SPAZI] DATA;N1;N2;N3;N4;N5;N6;JOLLY;STAR
    stringa_numeri = ";".join(sestina)
    dati_finali = f"{data_csv};{stringa_numeri};{j};{s}"

    # 4. GESTIONE FILE
    if not os.path.exists(file_path): return
    with open(file_path, 'r', encoding='utf-8') as f:
        righe = [line.strip() for line in f.readlines() if line.strip()]
        ultima_riga = righe[-1]

    if data_csv not in ultima_riga:
        # Prende l'indice all'inizio (es. 4280)
        ultimo_indice = int(ultima_riga.split()[0])
        nuovo_indice = ultimo_indice + 1
        
        # Scrive esattamente come le tue righe precedenti
        riga_da_scrivere = f"{nuovo_indice}   {dati_finali}"
        
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write('\n' + riga_da_scrivere)
        print(f"✅ RIGA AGGIUNTA CORRETTAMENTE: {riga_da_scrivere}")
    else:
        print(f"Estrazione del {data_csv} già presente.")

if __name__ == "__main__":
    update_csv()
