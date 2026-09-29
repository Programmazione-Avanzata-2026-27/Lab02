# LAB 02 DELLI CARRI LORENZO

def carica_da_file(file_path):
    dizfoto = {}
    try:
        with open(file_path, "r") as filefoto:
            filefoto.readline()

            for riga in filefoto:
                riga = riga.strip()
                if not riga:
                    continue

                campi = riga.split(",")
                codice = campi[0]
                titolo = campi[1]
                autore = campi[2]
                mese = int(campi[3])
                anno = int(campi[4])

                if anno not in dizfoto:
                    dizfoto[anno] = []
                dizfoto[anno].append([codice, titolo, autore, mese])

    except FileNotFoundError:
        return None

    return dizfoto


def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    if mese < 1 or mese > 12:
        return None

    for anno_presente in album:
        for foto in album[anno_presente]:
            if foto[0] == codice:
                return None

    try:
        with open(file_path, "a") as filefoto:
            filefoto.write(f"{codice},{titolo},{autore},{mese},{anno}\n")
    except FileNotFoundError:
        return None

    if anno not in album:
        album[anno] = []

    newfoto = [codice, titolo, autore, mese]
    album[anno].append(newfoto)

    return newfoto


def cerca_foto(album, codice):
    for anno in album:
        for foto in album[anno]:
            if foto[0] == codice:
                titolo = foto[1]
                autore = foto[2]
                mese = foto[3]
                return f"{codice}, {titolo}, {autore}, {mese}, {anno}"
    return None


def elenco_foto_anno_per_titolo(album, anno):
    if anno not in album:
        return None

    listatitoli = []
    for foto in album[anno]:
        listatitoli.append(foto[1])

    listatitoli.sort(reverse=False)

    return listatitoli


def main():
    album = {}
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
                album_caricato = carica_da_file(file_path)
                if album_caricato is not None:
                    album = album_caricato
                    print("Album caricato con successo!")
                    break
                else:
                    print("File non trovato. Riprova.")

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
                print(
                    "Non è stato possibile aggiungere la foto. Controlla che il codice non esista già o che il mese sia corretto.")

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