def carica_da_file(file_path):
    album = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            f.readline()

            for riga in f:
                # Evito problemi con eventuali righe vuote a fine file
                if not riga.strip():
                    continue

                elemento = riga.strip().split(',')
                codice = elemento[0]
                titolo = elemento[1]
                autore = elemento[2]
                mese = int(elemento[3])
                anno = int(elemento[4])

                # Creo la foto
                foto = {'codice': codice, 'titolo': titolo, 'autore': autore, 'mese': mese, 'anno': anno}

                # Organizziamo l'album usando l'ANNO come chiave
                if anno not in album:
                    album[anno] = []  # Creo la lista per il nuovo anno

                album[anno].append(foto)  # Aggiungo la foto alla lista di quell'anno

        return album

    except FileNotFoundError:
        return None


def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    # 1. Controllo mese
    if mese < 1 or mese > 12:
        return None

    # 2. Controllo se il codice esiste già
    for anno_esistente in album:
        for foto in album[anno_esistente]:
            if foto['codice'] == codice:
                return None

    # 3. Creazione del dizionario per la nuova foto
    nuova_foto = {
        'codice': codice,
        'titolo': titolo,
        'autore': autore,
        'mese': mese,
        'anno': anno
    }

    # 4. Scrittura su file
    try:

        with open(file_path, 'a', encoding='utf-8') as f:

            riga = f"{codice},{titolo},{autore},{mese},{anno}\n"
            f.write(riga)
    except FileNotFoundError:
        #  file non  trovato, l'operazione fallisce
        return None

    # 5. Aggiornamento del dizionario in memoria
    # Se l'anno non c'è ancora nell'album, creo una nuova lista vuota per quell'anno
    if anno not in album:
        album[anno] = []

    # Aggiungo la nuova foto alla lista di quell'anno
    album[anno].append(nuova_foto)


    return nuova_foto

    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""
    # TODO


def cerca_foto(album, codice):

    for anno in album:
        for foto in album[anno]:
            if foto['codice'] == codice:
                return f"{foto['codice']}, {foto['titolo']}, {foto['autore']}, {foto['mese']}, {foto['anno']}"
    return None



    """Cerca una foto nell'album dato il codice"""
    # TODO


def elenco_foto_anno_per_titolo(album, anno):
    if anno not in album: #nel testo dice che se l'anno non esiste di restituire None
        return None
    titoli = [] #creo la lista di titioli di foto
    for foto in album[anno]:
        titoli.append(foto['titolo'])
    return sorted(titoli)
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""
    # TODO


def main():
    album = []
    file_path = "album_fotografico.csv"
    album = carica_da_file(file_path)
    #print(album)



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
