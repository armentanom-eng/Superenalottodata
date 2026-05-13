import requests
import os
import re

def update_csv():
    file_path = 'storico_completo.csv'
    url = "https://www.superenalotto.net/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    try:
        r = requests.get(url, headers=headers, timeout=20)
        r.encoding = 'utf-8'
        html = r.text

        data_match = re.search(r'(\d{1,2})\s+(maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre|gennaio|febbraio|marzo|aprile)', html, re.IGNORECASE)
        if not data_match: return
        data_csv = f"{data_match.group(1).zfill(2)}-{data_match.group(2).lower()[:3]}"

        # Tagliamo l'HTML per cercare solo DOPO la data trovata
        pos_data = html.find(data_match.group(0))
        html_settore = html[pos_data:pos_data+2000] 

        # Troviamo TUTTI i numeri tra tag (es. <li>2</li> o <span>5</span>)
        numeri_trovati = re.findall(r'>(\d{1,2})<', html_settore)
        
        # Filtriamo: vogliamo solo numeri (evitiamo l'anno o il giorno se ripetuti)
        # In image_57.png i numeri sono i primi che appaiono in sequenza
        finali = []
        for n in numeri_trovati:
            if n not in finali or len(finali) < 6: # La sestina può avere duplicati in teoria, ma qui no
                finali.append(n.zfill(2))
            if len(finali) == 8: break

        if len(finali) == 8:
            sestina = ";".join(finali[:6])
            jolly = finali[6]
            star = finali[7]
            nuova_riga = f"{data_csv};{sestina};{jolly};{star}"

            with open(file_path, 'r', encoding='utf-8') as f:
                righe = [l.strip() for l in f.readlines() if l.strip()]
                ultima_riga = righe[-1]

            if data_csv not in ultima_riga:
                nuovo_indice = int(ultima_riga.split()[0]) + 1
                riga_finale = f"{nuovo_indice}   {nuova_riga}"
                with open(file_path, 'a', encoding='utf-8') as f:
                    f.write('\n' + riga_finale)
                print(f"✅ PRESI TUTTI E 8: {riga_finale}")
        else:
            print(f"Trovati solo {len(finali)} numeri dopo la data.")

    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    update_csv()
