import requests
import os
import re
import time

def update_csv():
    file_path = 'storico_completo.csv'
    url = "https://www.superenalotto.net/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15'
    }

    html = ""
    for i in range(3):
        try:
            r = requests.get(url, headers=headers, timeout=20)
            r.encoding = 'utf-8'
            if r.status_code == 200:
                html = r.text
                break
        except:
            time.sleep(5)
            continue

    if not html: return

    # 1. DATA (es. 12 maggio)
    data_match = re.search(r'(\d{1,2})\s+(maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre|gennaio|febbraio|marzo|aprile)', html, re.IGNORECASE)
    if not data_match: return
    
    data_csv = f"{data_match.group(1).zfill(2)}-{data_match.group(2).lower()[:3]}"

    # 2. NUMERI: Prendiamo TUTTE le palline in ordine
    # Cerchiamo tutti i numeri contenuti in tag <li> che hanno "ball" nella classe
    tutte_le_palline = re.findall(r'<li class="ball.*?">(\d{1,2})</li>', html)

    if len(tutte_le_palline) >= 8:
        sestina = tutte_le_palline[:6]
        jolly = tutte_le_palline[6]  # La 7ª pallina è il Jolly (5)
        star = tutte_le_palline[7]   # L'8ª pallina è la Star (2)
        
        corpo_dati = f"{data_csv};{';'.join(sestina)};{jolly};{star}"

        # 3. GESTIONE FILE
        if not os.path.exists(file_path): return
        with open(file_path, 'r', encoding='utf-8') as f:
            righe = [line.strip() for line in f.readlines() if line.strip()]
            ultima_riga = righe[-1]

        if data_csv not in ultima_riga:
            ultimo_indice = int(ultima_riga.split()[0])
            nuovo_indice = ultimo_indice + 1
            
            # Formato finale identico a riga 4280 (image_49.png)
            riga_finale = f"{nuovo_indice}   {corpo_dati}"
            
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write('\n' + riga_finale)
            print(f"✅ AGGIORNATO: {riga_finale}")
        else:
            print(f"Data {data_csv} già presente.")
    else:
        print(f"Trovate solo {len(tutte_le_palline)} palline. Struttura sito cambiata.")

if __name__ == "__main__":
    update_csv()
