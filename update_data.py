import os

def update_csv():
   file_path = 'storico_completo.csv'

   # DATI DALLA TUA FOTO (ADM 05/05/2026)
   # Formattati esattamente come li vuole l'app Flutter
   data_app = "05-mag"
   sestina = "24;34;45;55;81;87" # Li ho messi in ordine crescente
   jolly = "23"
   superstar = "52" 

   # Creiamo la riga (9 elementi: data + 6 numeri + jolly + superstar)
   nuova_riga = f"{data_app};{sestina};{jolly};{superstar}"

   try:
       # Leggiamo il file se esiste
       if os.path.exists(file_path):
           with open(file_path, 'r') as f:
               content = f.read()
       else:
           content = ""

       # Se il 05-mag c'è già, non facciamo nulla
       if data_app in content:
           print(f"L'estrazione del {data_app} è già presente.")
           return

       # Aggiungiamo la riga
       with open(file_path, 'a') as f:
           # Se il file non finisce con un invio, lo aggiungiamo noi
           if content and not content.endswith('\n'):
               f.write('\n')
           f.write(nuova_riga)

       print(f"SUCCESSO! Scritto nel CSV: {nuova_riga}")

   except Exception as e:
       print(f"Errore: {e}")
       exit(1) # Questo segnala errore a GitHub se qualcosa fallisce

if __name__ == "__main__":
   update_csv()
