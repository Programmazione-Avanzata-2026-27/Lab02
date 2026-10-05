import csv
from csv import reader

def aggiungi_foto(dizionario,anno,codice,titolo,autore,mese):
    if anno not in dizionario:
        dizionario[anno] = {}
    if 1<= int(mese) <=12:
        if codice not in dizionario[anno]:
            dizionario[anno][codice] = {"titolo" : titolo,
                "autore" : autore,
                "mese": mese}
            return f"All'album foto è stata aggiunta la foto {codice}-{titolo} di {autore} del {mese}/{anno}"
        else:
            return None
    else:
        return None

def carica_da_file(file):
    try:
        with open(file,"r",encoding = 'utf-8') as file:
            
            file = csv.reader(file)
            intestazione = next(file)
            dizionario = {}
            for indice,parola in enumerate(intestazione):
                if parola.strip().lower() == "codice":
                    posizione_codice = indice
                elif parola.strip().lower() == "titolo":
                    posizione_titolo = indice
                elif parola.strip().lower() == "mese":
                    posizione_mese = indice
                elif parola.strip().lower() == "anno":
                    posizione_anno = indice
                else:
                    posizione_autore = indice
            
            for foto in file:
                anno = foto[posizione_anno]
                codice = foto[posizione_codice]
                titolo = foto[posizione_titolo]
                autore = foto[posizione_autore]
                mese = foto[posizione_mese]
                if anno not in dizionario:
                    dizionario[anno] = {}
                    if 1<= int(mese) <=12:
                        if codice not in dizionario[anno]:
                            dizionario[anno][codice] = {"titolo" : titolo,
                "autore" : autore,
                "mese": mese}
        return dizionario
                
    except FileNotFoundError:
        return None

def cerca_foto(dizionario,codice):
    trovata = False
    for anno in dizionario:
        if codice not in dizionario[anno]:
            continue
        else:
            trovata = True
            stringa = f"{codice}"
            for i in dizionario[anno][codice]:
                stringa += f", {dizionario[anno][codice][i]}"
            break
    if trovata == False:
        return None
    else:
        return stringa

def elenco_foto_anno_per_titolo(dizionario,anno):
    lista = None
    if anno in dizionario:
        lista = []
        for codice in dizionario[anno]:
            lista.append(dizionario[anno][codice]["titolo"])
            
        lista.sort()
    return lista
def main():
    file = input("Inserire il file: ")
    dizionario = carica_da_file(file)
    if dizionario != None:
        cosa_fare = int(input("Digita 1 per Aggiungi foto.\nDigita 2 per Cerca foto.\nDigita 3 per Elenco foto anno per titolo\n"))
        if cosa_fare == 1:
            anno = input("Anno: ")
            mese = input("Mese: ")
            if int(mese)<1 or int(mese) > 12:
                print("Mese inesistente")
                exit()
            codice = input("Codice: ")
            titolo = input("Titolo: ")
            autore = input("Autore: ")
            stringa = aggiungi_foto(dizionario,str(anno),codice,titolo,autore,mese)
            if stringa != None:
                print(f"{stringa} è stata aggiunta correttamente")
            else:
                print(stringa," Foto non aggiunta correttamente")
        elif cosa_fare == 2:
            codice = input("Codice: ")
            foto = cerca_foto(dizionario,codice)
            print(foto)
        elif cosa_fare == 3:
            anno = (input("Anno: "))
            lista = elenco_foto_anno_per_titolo(dizionario,anno)
            if lista != None:
                for i in lista:
                    
                    print(i,end=' ')
            else:
                print(None)
        else:
            print("Azione non trovata\nScrivere come da elenco\n")
album_foto = main()
