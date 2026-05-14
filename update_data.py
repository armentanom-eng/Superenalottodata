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

        # 1. Estrazione DATA (gg-mese)
        data_match = re.search(r'(\d{1,2})\s+(maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre|gennaio|febbraio|marzo|aprile)', html, re.IGNORECASE)
        if not data_match: return
        data_csv = f"{data_match.group(1).zfill(2)}-{data_match.group(2).lower()[:3]}"

        # 2. Estrazione NUMERI (Struttura verificata da image_66.png)
        sestina = re.findall(r'class="ball">(\d{1,2})</li>', html)[:6]
        jolly = re.search(r'class="jolly">(\d{1,2})</li>', html)
        star = re.search(r'class="superstar">(\d{1,2})</li>', html)

        # Se i dati sul sito sono incompleti, non scrivere nulla
        if not (len(sestina) == 6 and jolly and star):
            print("Dati non pronti sul sito.")
            return

        # 3. Formattazione riga SENZA numero indice all'inizio
        n_lista = [n.zfill(2) for n in sestina]
        # Formato: DATA;N1;N2;N3;N4;N5;N6;JOLLY;STAR
        riga_finale = f"{data_csv};{';'.join(n_lista)};{jolly.group(1).zfill(2)};{star.group(1).zfill(2)}"

        # 4. Controllo duplicati e riga vuota
        if not os.path.exists(file_path): return

        with open(file_path, 'r', encoding='utf-8') as f:
            contenuto = f.read()
            righe = contenuto.strip().split('\n')
        
        # Se l'estrazione è già l'ultima riga, non aggiungerla di nuovo
        if righe and data_csv in righe[-1]:
            print("Estrazione già presente.")
            return

        # 5. Scrittura in Append ('a') - Sicura contro le cancellazioni
        # Aggiungiamo un a capo solo se il file non finisce già con uno
        separatore = "" if contenuto.endswith('\n') else "\n"
        
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(separatore + riga_finale)
            
        print(f"Aggiunta: {riga_finale}")

    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    update_csv()
