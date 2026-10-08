class Foto:
    def __init__(self, codice, titolo, autore, mese, anno):
        self.codice = codice
        self.titolo = titolo
        self.autore = autore
        self.mese = mese
        self.anno = anno

    def __str__(self):
        return f"{self.codice}, {self.titolo}, {self.autore}, {self.mese}, {self.anno}"