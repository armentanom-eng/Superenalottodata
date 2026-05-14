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
        if not data_match:
            print("Nessuna data trovata sul sito.")
            return
        
        data_csv = f"{data_match.group(1).zfill(2)}-{data_match.group(2).lower()[:3]}"

        # 2. Estrazione NUMERI (Struttura verificata da image_62.png)
        sestina = re.findall(r'class="ball">(\d{1,2})</li>', html)[:6]
        jolly = re.search(r'class="jolly">(\d{1,2})</li>', html)
        star = re.search(r'class="superstar">(\d{1,2})</li>', html)

        # CONTROLLO CRITICO: Se mancano i numeri (sito non aggiornato), NON SCRIVERE NULLA
        if not (len(sestina) == 6 and jolly and star):
            print("Numeri non ancora disponibili sul sito. Operazione annullata per evitare errori.")
            return

        # Preparazione stringa dati
        n_finali = [n.zfill(2) for n in sestina]
        j_val = jolly.group(1).zfill(2)
        s_val = star.group(1).zfill(2)
        corpo_estrazione = f"{data_csv};{';'.join(n_finali)};{j_val};{s_val}"

        # 3. Lettura dell'ultimo indice (SENZA riscrittura del file)
        if not os.path.exists(file_path):
            print(f"Errore: {file_path} non trovato.")
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            linee = [l.strip() for l in f.readlines() if l.strip()]
        
        ultimo_indice = 0
        if linee:
            # Cerchiamo l'ultimo indice valido scorrendo dal basso
            for riga in reversed(linee):
                parti = riga.split(';')
                if parti[0].isdigit():
                    ultimo_indice = int(parti[0])
                    break
        
        # 4. AGGIUNTA (APPEND) - Forza l'aggiunta indipendentemente dalla data
        nuovo_indice = ultimo_indice + 1
        riga_da_scrivere = f"{nuovo_indice};{corpo_estrazione}"
        
        with open(file_path, 'a', encoding='utf-8') as f:
            # Assicuriamoci di andare a capo prima di scrivere la nuova riga
            f.write('\n' + riga_da_scrivere)
            
        print(f"✅ Estrazione aggiunta con successo: {riga_finale}")

    except Exception as e:
        print(f"Errore durante l'esecuzione: {e}")

if __name__ == "__main__":
    update_csv()
