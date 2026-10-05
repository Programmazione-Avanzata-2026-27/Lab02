
import csv
def carica_da_file(file_path):
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""
    try:
        with open(file_path, "r", encoding = "utf-8") as fotografie:
            file = csv.reader(fotografie)
            album = {}  #Album come dizionario così individuo una lista per ogni anno
            next(file)  #Salto l'intestazione
            for foto in file:
                a = int(foto[4])
                codice = foto[0]

                if a not in album:
                    album[a] = {}

                #Dato che la ricerca foto avviene tramite codice mi conviene utilizzare la seguente
                #struttura Album --> Anno --> Codice --> Resto delle informazioni
                #Implemento un dizionario nel dizionario dei mesi a cui collego una lista

                album[a][codice] = foto[1:4]

        return album

    except FileNotFoundError:
        return None


import csv


def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""
    if int(mese) < 1 or int(mese) > 12:
        return None

    for a in album:
        if codice in album[a]:
            return None

    if anno not in album:
        album[anno] = {}
    album[anno][codice] = [titolo, autore, mese]

    try:
        with open(file_path, "a", newline="", encoding="utf-8") as fotografie:
            writer = csv.writer(fotografie)
            writer.writerow([codice, titolo, autore, mese, anno])

        return True

    except FileNotFoundError:
        return None

def cerca_foto(album, codice):
    """Cerca una foto nell'album dato il codice"""
    for anno in album:
        if codice in album[anno]:
            riga = [codice, album[anno][codice]]
            return riga

    return None


def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""
    Titoli = list()
    for i in album[anno]:
        Titoli.append(album[anno][i][0])

    Titoli_ordinati = sorted(Titoli)
    return Titoli_ordinati

def main():
    album = {} #Cambiato in dizionario
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                if album is not None:
                    break

        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()
