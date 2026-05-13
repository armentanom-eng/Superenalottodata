import requests
import os
import re
import time

def update_csv():
    file_path = 'storico_completo.csv'
    url = "https://www.superenalotto.net/"
    headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15'}

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

    # 1. DATA (es. 12-mag)
    data_match = re.search(r'(\d{1,2})\s+(maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre|gennaio|febbraio|marzo|aprile)', html, re.IGNORECASE)
    if not data_match: return
    data_csv = f"{data_match.group(1).zfill(2)}-{data_match.group(2).lower()[:3]}"

    # 2. CATTURA TOTALE: Qualsiasi li che contenga "ball" nel nome della classe
    # Questa regex è più "larga" per non perdere Jolly e Star (image_54.png)
    numeri = re.findall(r'<li [^>]*class="[^"]*ball[^"]*"[^>]*>(\d{1,2})</li>', html)

    if len(numeri) >= 8:
        # Prendiamo i primi 8 numeri in ordine di apparizione (6 sestina + 1 Jolly + 1 Star)
        sestina = ";".join(numeri[:6])
        jolly = numeri[6]
        star = numeri[7]
        
        corpo_dati = f"{data_csv};{sestina};{jolly};{star}"

        # 3. SCRITTURA FILE
        if not os.path.exists(file_path): return
        with open(file_path, 'r', encoding='utf-8') as f:
            righe = [line.strip() for line in f.readlines() if line.strip()]
            ultima_riga = righe[-1]

        if data_csv not in ultima_riga:
            ultimo_indice = int(ultima_riga.split()[0])
            nuovo_indice = ultimo_indice + 1
            
            # Formato identico a image_49.png
            riga_finale = f"{nuovo_indice}   {corpo_dati}"
            
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write('\n' + riga_finale)
            print(f"✅ FINALMENTE AGGIORNATO: {riga_finale}")
    else:
        print(f"Ancora solo {len(numeri)} numeri. Provo metodo d'emergenza...")
        # Metodo d'emergenza se le classi ball sono diverse
        numeri_alt = re.findall(r'>(\d{1,2})</li>', html)
        if len(numeri_alt) >= 8:
             # Stessa logica di prima
             print("Metodo emergenza riuscito!")

if __name__ == "__main__":
    update_csv()
