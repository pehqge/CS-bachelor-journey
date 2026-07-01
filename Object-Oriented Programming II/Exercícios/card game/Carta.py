from AbstractCarta import AbstractCarta
from Personagem import Personagem


class Carta(AbstractCarta):
    def __init__(self, personagem: Personagem):
        if isinstance(personagem, Personagem):
            self.__personagem = personagem

    @property
    def personagem(self):
        return self.__personagem

    def valor_total_carta(self):
        soma = (self.personagem.energia
                + self.personagem.habilidade
                + self.personagem.velocidade
                + self.personagem.resistencia)
        return soma
