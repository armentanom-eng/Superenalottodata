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

        # 1. Trova la DATA (es. 12 maggio)
        data_match = re.search(r'(\d{1,2})\s+(maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre|gennaio|febbraio|marzo|aprile)', html, re.IGNORECASE)
        if not data_match: return
        data_csv = f"{data_match.group(1).zfill(2)}-{data_match.group(2).lower()[:3]}"

        # 2. Trova i NUMERI (Classi ball, jolly, superstar viste su PC)
        sestina = re.findall(r'class="ball">(\d{1,2})</li>', html)[:6]
        jolly = re.search(r'class="jolly">(\d{1,2})</li>', html)
        star = re.search(r'class="superstar">(\d{1,2})</li>', html)

        if len(sestina) == 6 and jolly and star:
            n_finali = [n.zfill(2) for n in sestina]
            j_val = jolly.group(1).zfill(2)
            s_val = star.group(1).zfill(2)
            # Formato: DATA;N1;N2;N3;N4;N5;N6;JOLLY;STAR
            corpo_estrazione = f"{data_csv};{';'.join(n_finali)};{j_val};{s_val}"

            # 3. GESTIONE CSV E PULIZIA ERRORI
            if not os.path.exists(file_path): return
            
            with open(file_path, 'r', encoding='utf-8') as f:
                righe_grezze = f.readlines()
            
            # Filtriamo solo le righe che iniziano con un numero valido (evitiamo il crash di image_65.png)
            righe_valide = []
            ultimo_indice = 0
            
            for riga in righe_grezze:
                riga = riga.strip()
                if not riga: continue
                
                # Prova a estrarre l'indice iniziale
                parti = riga.split(';')
                if parti[0].isdigit():
                    ultimo_indice = int(parti[0])
                    righe_valide.append(riga)
                else:
                    # Se la riga è "sporca" (es. inizia con 09-mag), la ignoriamo e non la salviamo
                    continue
            
            # Prepariamo la nuova riga
            nuovo_indice = ultimo_indice + 1
            riga_finale = f"{nuovo_indice};{corpo_estrazione}"
            
            # Scrittura finale: rigenera il file pulito + la nuova estrazione
            with open(file_path, 'w', encoding='utf-8') as f:
                for riga in righe_valide:
                    f.write(riga + '\n')
                f.write(riga_finale)
            
            print(f"✅ FILE RIPULITO E AGGIORNATO: {riga_finale}")
        
    except Exception as e:
        print(f"Errore tecnico: {e}")

if __name__ == "__main__":
    update_csv()
