from AbstractControladorJogo import *
import random


class ControladorJogo(AbstractControladorJogo):
    def __init__(self):
        self.__baralho = []
        self.__personagems = []

    @property
    def baralho(self) -> list:
        return self.__baralho

    @property
    def personagems(self) -> list:
        return self.__personagems

    def inclui_personagem_na_lista(self,
                                   energia: int,
                                   habilidade: int,
                                   velocidade: int,
                                   resistencia: int,
                                   tipo: Tipo) -> Personagem:
        personagem = Personagem(energia, habilidade,
                                velocidade, resistencia, tipo)
        self.personagems.append(personagem)
        return personagem

    def inclui_carta_no_baralho(self, personagem: Personagem) -> Carta:
        carta = Carta(personagem)
        self.baralho.append(carta)
        return carta

    def iniciaJogo(self, jogador1: Jogador, jogador2: Jogador):
        if self.baralho > 0:
            for _ in range(5):
                jogador1.inclui_carta_na_mao(random.choice(self.mao))
                jogador2.inclui_carta_na_mao(random.choice(self.mao))

    def jogada(self, mesa: Mesa) -> Jogador:
        jogador1 = mesa.jogador1
        jogador2 = mesa.jogador2
        cartaj1 = mesa.carta_jogador1
        cartaj2 = mesa.carta_jogador2
        if cartaj1.valor_total_carta() > cartaj2.valor_total_carta():
            jogador1.inclui_carta_na_mao(cartaj1)
            jogador1.inclui_carta_na_mao(cartaj2)
        elif cartaj1.valor_total_carta() < cartaj2.valor_total_carta():
            jogador2.inclui_carta_na_mao(cartaj1)
            jogador2.inclui_carta_na_mao(cartaj2)
        else:
            jogador1.inclui_carta_na_mao(cartaj1)
            jogador2.inclui_carta_na_mao(cartaj2)
        if jogador1.mao == []:
            return jogador2
        elif jogador2.mao == []:
            return jogador1
        else:
            return None
