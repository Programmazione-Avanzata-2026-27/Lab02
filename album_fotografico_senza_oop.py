def cerca_elemento_anno(album, anno):
    for elemento_anno in album:
        if elemento_anno[0] == anno:
            return elemento_anno
    return None


def carica_da_file(file_path):
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""

    album = [] # Collezione di elemento_anno

    try:
        file = open(file_path, "r")
        file.readline() # Legge la prima riga con intest., non la uso
        for riga in file:
            riga.strip()
            campi = riga.split(",") # Campi di una riga
            codice = campi[0] # Il primo campo, codice
            titolo = campi[1]
            autore = campi[2]
            mese = int(campi[3])
            anno = int(campi[4])

            foto = [codice, titolo, autore, mese, anno]
            # Qui ho una foto, cosa me ne faccio?

            # Posso fare una lista dove ogni elemento della lista
            # è formato da anno e dalla lista di foto per quell'anno
            # (e poi ogni foto a sua volta è una lista di campi)
            # elemento_anno = [anno, []]

            elemento_anno = cerca_elemento_anno(album, anno)
            if elemento_anno is None: # Non c'era ancora
                elemento_anno = [anno, []] # Creo un elemento_anno per quell'anno con lista di foro vuota
                album.append(elemento_anno) # E aggiungo quell'elemento_anno all'album

            # Sia che ci fosse già sia che l'abbia crerato adesso, gli appendo la foto
            elemento_anno[1].append(foto) # elemento_anno[1] è una lista di foto

        file.close()
        print(album)
        return album


    except FileNotFoundError:
        print("Errore nell'apertura del file")
        return None


def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""

    if mese < 1 or mese > 12:
       return None

    if cerca_foto(album, codice) is not None: # Se la foto c'è già
        return None # Esco dalla funzione

    # Se sono qui vuol dire che la foto è da aggiungere (in memoria e nel file)

    nuova_foto = [codice, titolo, autore, mese, anno]

    try:
        with open(file_path, "a") as file: # Append in coda
            file.write(f"{codice},{titolo},{autore},{mese},{anno}\n")
    except FileNotFoundError:
        print("Errore nell'apertura del file")

    elemento_anno = cerca_elemento_anno(album, anno)
    if elemento_anno is None:
        elemento_anno = [anno, []]
    elemento_anno[1].append(nuova_foto)

    return nuova_foto

def cerca_foto(album, codice):
    """Cerca una foto nell'album dato il codice"""
    for elemento_anno in album: # elemento_anno = [anno, [<foto><foto>]]
        for foto in elemento_anno[1]:
            if foto[0] == codice:
                return f"{foto[0]}, {foto[1]}, {foto[2]}, {foto[3]}, {foto[4]}"

    return None

def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""

    titoli = []
    for elemento_anno in album:
        if elemento_anno[0] == anno: # Solo le foto dell'anno passato come par.
            for foto in elemento_anno[1]:
                titoli.append(foto[1]) # titolo

    titoli.sort()  # Ordino la lista di titoli stessa
    return titoli

def main():
    album = []
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
