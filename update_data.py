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
        
        data_csv = f"{data_match.group(1).zfill(2)}-{data_match.group(2).lower()[:3]}"

        # 2. Trova i NUMERI (Basato sulla struttura esatta di image_62.png)
        # Sestina: class="ball"
        sestina = re.findall(r'class="ball">(\d{1,2})</li>', html)[:6]
        # Jolly: class="jolly"
        jolly_match = re.search(r'class="jolly">(\d{1,2})</li>', html)
        # Superstar: class="superstar"
        star_match = re.search(r'class="superstar">(\d{1,2})</li>', html)

        if len(sestina) == 6 and jolly_match and star_match:
            # Puliamo i numeri togliendo eventuali zeri inutili e rimettendo il zfill(2) per il CSV
            n_lista = [n.zfill(2) for n in sestina]
            jolly = jolly_match.group(1).zfill(2)
            star = star_match.group(1).zfill(2)

            stringa_estrazione = f"{data_csv};{';'.join(n_lista)};{jolly};{star}"

            # 3. Scrittura nel CSV con Indice Progressivo all'INIZIO
            if not os.path.exists(file_path): return
            with open(file_path, 'r', encoding='utf-8') as f:
                righe = [l.strip() for l in f.readlines() if l.strip()]
                ultima_riga = righe[-1]

            if data_csv not in ultima_riga:
                # Prende l'indice progressivo (prima parola della riga)
                ultimo_indice = int(ultima_riga.split()[0])
                nuovo_indice = ultimo_indice + 1
                
                # Formato INDICE + 3 SPAZI + DATI
                riga_finale = f"{nuovo_indice}   {stringa_estrazione}"
                
                with open(file_path, 'a', encoding='utf-8') as f:
                    f.write('\n' + riga_finale)
                print(f"✅ AGGIORNATO CON SUCCESSO: {riga_finale}")
            else:
                print(f"L'estrazione del {data_csv} è già presente.")
        else:
            print(f"Errore cattura: Sestina={len(sestina)}, Jolly={'OK' if jolly_match else 'NO'}, Star={'OK' if star_match else 'NO'}")

    except Exception as e:
        print(f"Errore tecnico: {e}")

if __name__ == "__main__":
    update_csv()
