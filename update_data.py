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

        # 1. Estrazione DATA dal sito (formato gg-mese)
        data_match = re.search(r'(\d{1,2})\s+(maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre|gennaio|febbraio|marzo|aprile)', html, re.IGNORECASE)
        if not data_match: 
            print("Data non trovata sul sito.")
            return
        
        data_csv = f"{data_match.group(1).zfill(2)}-{data_match.group(2).lower()[:3]}"

        # 2. Estrazione NUMERI (basata sulla struttura di image_66.png)
        sestina = re.findall(r'class="ball">(\d{1,2})</li>', html)[:6]
        jolly = re.search(r'class="jolly">(\d{1,2})</li>', html)
        star = re.search(r'class="superstar">(\d{1,2})</li>', html)

        # Se i numeri non sono ancora pronti (palline vuote), usciamo senza fare nulla
        if not (len(sestina) == 6 and jolly and star):
            print(f"Estrazione del {data_csv} non ancora completa sul sito.")
            return

        # 3. CONTROLLO MIRATO SOLO SULL'ULTIMA RIGA
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                # Leggiamo tutte le linee e rimuoviamo quelle vuote
                linee = [l.strip() for l in f.readlines() if l.strip()]
            
            if linee:
                ultima_riga = linee[-1] # Prende esclusivamente l'ultima riga esistente
                # Se l'ultima riga inizia con la data di oggi, si ferma immediatamente
                if ultima_riga.startswith(data_csv):
                    print(f"L'estrazione del {data_csv} è già presente come ultima riga. Salto.")
                    return

        # 4. PREPARAZIONE STRINGA (Formato: DATA;N1;N2;N3;N4;N5;N6;JOLLY;STAR)
        n_lista = [n.zfill(2) for n in sestina]
        riga_finale = f"{data_csv};{';'.join(n_lista)};{jolly.group(1).zfill(2)};{star.group(1).zfill(2)}"

        # 5. SCRITTURA IN APPEND (Sicura al 100% contro le cancellazioni)
        with open(file_path, 'r', encoding='utf-8') as f:
            testo_completo = f.read()
        
        # Gestione intelligente dell'andata a capo
        separatore = "" if testo_completo.endswith('\n') or not testo_completo else "\n"
        
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(separatore + riga_finale)
            
        print(f"✅ Successo! Aggiunta riga: {riga_finale}")

    except Exception as e:
        print(f"Errore durante l'esecuzione: {e}")

if __name__ == "__main__":
    update_csv()
