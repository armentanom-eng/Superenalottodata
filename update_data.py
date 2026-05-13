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
        if not data_match: return
        
        data_csv = f"{data_match.group(1).zfill(2)}-{data_match.group(2).lower()[:3]}"

        # 2. TROVA TUTTI I NUMERI (Sestina + Jolly + Star)
        # Cerchiamo qualsiasi numero contenuto tra <li> e </li> che abbia "ball" nel tag
        tutti_i_numeri = re.findall(r'<li [^>]*ball[^>]*>(\d{1,2})</li>', html)

        if len(tutti_i_numeri) >= 8:
            # Prendiamo i primi 8 in ordine: 0,1,2,3,4,5 (sestina), 6 (jolly), 7 (star)
            numeri_puliti = [str(int(n)) for n in tutti_i_numeri] # Toglie lo zero davanti se presente
            
            sestina = ";".join(numeri_puliti[:6])
            jolly = numeri_puliti[6]
            star = numeri_puliti[7]

            stringa_estrazione = f"{data_csv};{sestina};{jolly};{star}"

            # 3. Scrittura nel CSV con Indice all'inizio
            if not os.path.exists(file_path): return
            with open(file_path, 'r', encoding='utf-8') as f:
                righe = [l.strip() for l in f.readlines() if l.strip()]
                ultima_riga = righe[-1]

            if data_csv not in ultima_riga:
                ultimo_indice = int(ultima_riga.split()[0])
                nuovo_indice = ultimo_indice + 1
                
                # Formato identico a riga 4280: INDICE [SPAZI] DATI
                riga_finale = f"{nuovo_indice}   {stringa_estrazione}"
                
                with open(file_path, 'a', encoding='utf-8') as f:
                    f.write('\n' + riga_finale)
                print(f"✅ AGGIORNATO: {riga_finale}")
        else:
            print(f"Trovati solo {len(tutti_i_numeri)} numeri. Struttura incompleta.")

    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    update_csv()
