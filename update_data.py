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

        # 1. Estrazione DATA
        data_match = re.search(r'(\d{1,2})\s+(maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre|gennaio|febbraio|marzo|aprile)', html, re.IGNORECASE)
        if not data_match: return
        data_csv = f"{data_match.group(1).zfill(2)}-{data_match.group(2).lower()[:3]}"

        # 2. Estrazione NUMERI
        sestina = re.findall(r'class="ball">(\d{1,2})</li>', html)[:6]
        jolly = re.search(r'class="jolly">(\d{1,2})</li>', html)
        star = re.search(r'class="superstar">(\d{1,2})</li>', html)

        if not (len(sestina) == 6 and jolly and star):
            print("Dati incompleti sul sito. Salto.")
            return

        # 3. Calcolo INDICE (Migliorato per gestire image_68.png)
        with open(file_path, 'r', encoding='utf-8') as f:
            linee = [l.strip() for l in f.readlines() if l.strip()]
        
        ultimo_indice = 0
        for riga in reversed(linee):
            # Cerchiamo il primo numero all'inizio della riga
            match_idx = re.match(r'^(\d+)', riga)
            if match_idx:
                ultimo_indice = int(match_idx.group(1))
                break
        
        # 4. Formattazione riga (Niente spazi, formato preciso)
        nuovo_indice = ultimo_indice + 1
        n_lista = [n.zfill(2) for n in sestina]
        # Forza il formato: INDICE;DATA;NUMERI;JOLLY;STAR
        riga_finale = f"{nuovo_indice};{data_csv};{';'.join(n_lista)};{jolly.group(1).zfill(2)};{star.group(1).zfill(2)}"

        # 5. Scrittura pulita (Evita riga vuota se non necessaria)
        with open(file_path, 'r', encoding='utf-8') as f:
            contenuto = f.read()
        
        # Se il file non finisce già con un a capo, lo aggiungiamo noi
        separatore = "" if contenuto.endswith('\n') else "\n"
        
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(separatore + riga_finale)
            
        print(f"Inserito correttamente: {riga_finale}")

    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    update_csv()
