from mamifero import Mamifero


class Gato(Mamifero):
    def __init__(self):
        super().__init__(2, 2)

    def produzirSom(self):
        return f"MAMIFERO: PRODUZ SOM: {self.volumeSom} SOM: "

    def miar(self):
        return self.produzirSom()+"MIAU"
