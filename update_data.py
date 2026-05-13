import requests
import os
import re

def update_csv():
    file_path = 'storico_completo.csv'
    url = "https://www.superenalotto.net/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        r = requests.get(url, headers=headers, timeout=20)
        r.encoding = 'utf-8'
        html = r.text

        # 1. Trova la DATA (es. 12 maggio)
        data_match = re.search(r'(\d{1,2})\s+(maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre|gennaio|febbraio|marzo|aprile)', html, re.IGNORECASE)
        if not data_match:
            print("Data non trovata.")
            return
        
        gg = data_match.group(1).zfill(2)
        mese_nome = data_match.group(2).lower()[:3] 
        data_csv = f"{gg}-{mese_nome}"

        # 2. Trova i NUMERI (Sestina, Jolly e Superstar)
        # Cerchiamo separatamente per via delle classi diverse viste nel sito (image_57.png)
        sestina = re.findall(r'<li class="ball">(\d{1,2})</li>', html)[:6]
        jolly_match = re.search(r'class="ball\s+jolly">(\d{1,2})</li>', html)
        star_match = re.search(r'class="ball\s+superstar">(\d{1,2})</li>', html)

        if len(sestina) < 6 or not jolly_match or not star_match:
            print("Dati estrazione incompleti.")
            return

        # Pulizia numeri (senza zeri davanti per i singoli numeri come da image_49.png)
        n_lista = [str(int(n)) for n in sestina]
        jolly = str(int(jolly_match.group(1)))
        star = str(int(star_match.group(1)))

        # Formato: DATA;N1;N2;N3;N4;N5;N6;JOLLY;STAR
        stringa_estrazione = f"{data_csv};{';'.join(n_lista)};{jolly};{star}"

        # 3. Gestione CSV e Indice Progressivo all'INIZIO
        if not os.path.exists(file_path): return

        with open(file_path, 'r', encoding='utf-8') as f:
            righe = [l.strip() for l in f.readlines() if l.strip()]
            ultima_riga = righe[-1]

        if data_csv not in ultima_riga:
            # Prende il primo elemento della riga (l'indice progressivo)
            try:
                ultimo_indice = int(ultima_riga.split()[0])
                nuovo_indice = ultimo_indice + 1
            except:
                nuovo_indice = 1
            
            # Formattazione finale: INDICE + 3 SPAZI + DATI (come image_49.png)
            riga_finale = f"{nuovo_indice}   {stringa_estrazione}"
            
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write('\n' + riga_finale)
            print(f"✅ AGGIORNATO CORRETTAMENTE: {riga_finale}")
        else:
            print(f"Estrazione del {data_csv} già presente.")

    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    update_csv()
