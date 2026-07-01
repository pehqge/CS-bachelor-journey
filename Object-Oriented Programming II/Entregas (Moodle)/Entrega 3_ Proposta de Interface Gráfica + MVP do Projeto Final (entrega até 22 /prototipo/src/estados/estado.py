from abc import ABC, abstractmethod
import pygame

# Classe base para os estados do jogo
class Estado(ABC):
    # Recebe uma referẽncia do jogo 
    def __init__(self, game_ref) -> None:
        self.__game = game_ref

    # Renderiza a tela em cada estado
    @abstractmethod
    def render(self) -> None:
        pass

    # Atualiza os objetos da tela em cada estado a cada frame
    @abstractmethod
    def update(self, event) -> None:
        pass

    # É chamado ao entrar em um determinado estado
    @abstractmethod
    def entering(self) -> None:
        pass

    # É chamado ao sair de um determinado estado
    @abstractmethod
    def exiting(self) -> None:
        pass
    
    @property
    def game(self):
        return self.__game