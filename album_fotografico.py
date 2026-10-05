def carica_da_file(file_path):
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""
    album = []
    try:
        file = open(file_path, "r", encoding="utf-8")
        for linea in file:
            linea = linea.rstrip()
            if linea != "":
                parti = linea.split(",")
                if len(parti) >= 5:
                    if parti[0].lower() != "codice":
                        codice = parti[0].rstrip()
                        titolo = parti[1].rstrip()
                        autore = parti[2].rstrip()

                        try:
                            mese = int(parti[3].rstrip())
                            anno = int(parti[4].rstrip())

                            anno_trovato = False
                            for elemento in album:
                                if elemento["anno"] == anno:
                                    elemento["foto"].append({
                                        "codice": codice,
                                        "titolo": titolo,
                                        "autore": autore,
                                        "mese": mese
                                    })
                                    anno_trovato = True

                            if anno_trovato == False:
                                album.append({
                                    "anno": anno,
                                    "foto": [{
                                        "codice": codice,
                                        "titolo": titolo,
                                        "autore": autore,
                                        "mese": mese
                                    }]
                                })

                        except ValueError:
                            errore = True
        file.close()
        print("Album caricato correttamente.")
    except FileNotFoundError:
        print("File non trovato. Verrà avviato un album vuoto.")
    except Exception as e:
        print(f"Errore durante la lettura: {e}")

    return album
    # TODO


def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""
    anno_trovato = False

    try:
        for elemento in album:
            if elemento["anno"] == anno:
                elemento["foto"].append({
                    "codice": codice,
                    "titolo": titolo,
                    "autore": autore,
                    "mese": mese
                })
                anno_trovato = True

        if anno_trovato == False:
            album.append({
                "anno": anno,
                "foto": [{
                    "codice": codice,
                    "titolo": titolo,
                    "autore": autore,
                    "mese": mese
                }]
            })

        file = open(file_path, "a", encoding="utf-8")
        file.write(f"{codice},{titolo},{autore},{mese},{anno}\n")
        file.close()
        return True
    except Exception as e:
        print(f"Errore durante il salvataggio sul file: {e}")
        return False
    # TODO


def cerca_foto(album, codice):
    """Cerca una foto nell'album dato il codice"""
    risultato = ""
    for elemento in album:
        for foto in elemento["foto"]:
            if foto["codice"] == codice:
                risultato = f"Titolo: '{foto['titolo']}' | Autore: {foto['autore']} | Mese: {foto['mese']} | Anno: {elemento['anno']}"

    return risultato
    # TODO


def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""
    titoli = []
    for elemento in album:
        if elemento["anno"] == anno:
            for foto in elemento["foto"]:
                titoli.append(foto["titolo"])

            titoli.sort()

    return titoli
    # TODO


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
