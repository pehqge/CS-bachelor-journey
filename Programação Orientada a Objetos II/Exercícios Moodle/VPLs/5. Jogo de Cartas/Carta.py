from AbstractCarta import *
from Personagem import *


class Carta(AbstractCarta):
    def __init__(self, personagem: Personagem):
        if isinstance(personagem, Personagem):
            self.__personagem = personagem

    def valor_total_carta(self) -> int:
        valor = (self.personagem.energia
                 + self.personagem.habilidade
                 + self.personagem.velocidade
                 + self.personagem.resistencia)
        return valor

    @property
    def personagem(self) -> Personagem:
        return self.__personagem
