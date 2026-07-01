from src.estados.estado import Estado
from src.fase.fase import Fase
from src.fase.mapas import Mapa
import pygame

class Jogo(Estado):
    def __init__(self, game):
        super().__init__(game)
        self.__fase = Fase(Mapa().mapa[0], self.game, 0) # Cria várias fases com todos os mapas possíveis dentro da classe Mapas. Se quiser aumentar o número de fases, basta adicionar mais mapas na classe Mapas.
        
    def entering(self):
        pass
    
    def exiting(self):
        pass
    
    def update(self, event):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.define_estado('menu')
            self.__fase.run()
    
    def render(self):
        pass