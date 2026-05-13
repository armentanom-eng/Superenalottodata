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
        
        gg = data_match.group(1).zfill(2)
        mese_nome = data_match.group(2).lower()[:3] 
        data_csv = f"{gg}-{mese_nome}"

        # 2. Trova TUTTI i numeri (ne cerchiamo 8 in totale)
        # La regex ora dice: prendi il numero dentro qualsiasi tag <li> che abbia la parola "ball" nella classe
        tutti_i_numeri = re.findall(r'<li [^>]*ball[^>]*>(\d{1,2})</li>', html)

        if len(tutti_i_numeri) >= 8:
            # Prendiamo i primi 8 in ordine cronologico di apparizione sulla pagina
            numeri_puliti = [n.zfill(2) for n in tutti_i_numeri[:8]]
            
            sestina = ";".join(numeri_puliti[:6]) # I primi 6
            jolly = numeri_puliti[6]             # Il 7°
            star = numeri_puliti[7]              # L'8°

            nuova_riga_dati = f"{data_csv};{sestina};{jolly};{star}"

            # 3. Gestione CSV e Indice Progressivo (all'inizio)
            if not os.path.exists(file_path): return

            with open(file_path, 'r', encoding='utf-8') as f:
                righe = [l.strip() for l in f.readlines() if l.strip()]
                ultima_riga = righe[-1]

            if data_csv not in ultima_riga:
                # Estraiamo l'indice (il primo numero della riga)
                ultimo_indice = int(ultima_riga.split()[0])
                nuovo_indice = ultimo_indice + 1
                
                # Formato: INDICE + 3 SPAZI + DATI
                riga_finale = f"{nuovo_indice}   {nuova_riga_dati}"
                
                with open(file_path, 'a', encoding='utf-8') as f:
                    f.write('\n' + riga_finale)
                print(f"✅ AGGIORNATO: {riga_finale}")
            else:
                print(f"Estrazione del {data_csv} già presente.")
        else:
            print(f"Trovati solo {len(tutti_i_numeri)} numeri. Struttura sito variata.")

    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    update_csv()
