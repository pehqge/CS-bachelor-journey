from mamifero import Mamifero


class Cachorro(Mamifero):
    def __init__(self):
        super().__init__(3, 3)

    def produzirSom(self):
        return f"MAMIFERO: PRODUZ SOM: {self.volumeSom} SOM: "

    def latir(self):
        return self.produzirSom() + "AU"
