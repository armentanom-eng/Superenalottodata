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

        # 1. DATA - Cerchiamo la prima data utile che appare (quella più recente)
        data_match = re.search(r'(\d{1,2})\s+(maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre|gennaio|febbraio|marzo|aprile)', html, re.IGNORECASE)
        if not data_match: return
        data_csv = f"{data_match.group(1).zfill(2)}-{data_match.group(2).lower()[:3]}"

        # 2. NUMERI - Struttura Chrome PC (image_62.png)
        sestina = re.findall(r'class="ball">(\d{1,2})</li>', html)[:6]
        jolly = re.search(r'class="jolly">(\d{1,2})</li>', html)
        star = re.search(r'class="superstar">(\d{1,2})</li>', html)

        if len(sestina) == 6 and jolly and star:
            n_finali = [n.zfill(2) for n in sestina]
            j_val = jolly.group(1).zfill(2)
            s_val = star.group(1).zfill(2)
            corpo_dati = f"{data_csv};{';'.join(n_finali)};{j_val};{s_val}"

            # 3. SCRITTURA E PULIZIA INDICE
            if not os.path.exists(file_path): return
            with open(file_path, 'r', encoding='utf-8') as f:
                righe = [l.strip() for l in f.readlines() if l.strip()]
            
            # Troviamo l'ultimo indice valido scorrendo dal basso
            ultimo_indice = 0
            for riga in reversed(righe):
                parti = riga.split()
                if parti and parti[0].isdigit():
                    ultimo_indice = int(parti[0])
                    break
            
            # Verifichiamo se la data è già nell'ultima riga
            if data_csv not in righe[-1]:
                nuovo_indice = ultimo_indice + 1
                riga_finale = f"{nuovo_indice}   {corpo_dati}"
                
                with open(file_path, 'a', encoding='utf-8') as f:
                    f.write('\n' + riga_finale)
                print(f"✅ REGISTRATA: {riga_finale}")
            else:
                print(f"Estrazione {data_csv} già presente.")
        
    except Exception as e:
        print(f"Errore tecnico: {e}")

if __name__ == "__main__":
    update_csv()
