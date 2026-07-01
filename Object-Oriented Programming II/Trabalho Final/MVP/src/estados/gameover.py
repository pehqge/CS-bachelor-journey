import pygame
import sys
from src.estados.estado import Estado
from src.estados.botao import Botao
from src.fase.mapas import Mapa

class GameOverState(Estado):
    def __init__(self, game):
        super().__init__(game)
        # CARREGAMENTO DOS ASSETS DO MENU
        background = pygame.image.load('assets/backgrounds/menu.png').convert_alpha()
        self.__background = pygame.transform.scale(background, (Mapa().largura_tela, Mapa().altura_tela))
        self.__texto = pygame.image.load('assets/texto_parabens.png').convert_alpha()
        img_botao_menu = pygame.image.load('assets/botoes/menu.png').convert_alpha()
        img_botao_sair = pygame.image.load('assets/botoes/sair.png').convert_alpha()
        self.__botoes = {'menu': Botao((self.game.largura_tela - img_botao_menu.get_width())//4 , 500, img_botao_menu, 1), 
                         'sair': Botao((self.game.largura_tela - img_botao_sair.get_width())*3//4, 500, img_botao_sair, 1)}
        

    def entering(self):
        pass
            
    def exiting(self):
        pass

    def update(self, event):
        if self.__botoes['sair'].clicado():
            pygame.quit()
            sys.exit()
            
        if self.__botoes['menu'].clicado():
            self.game.define_estado('menu')
                
    def render(self):
        self.game.screen.fill('White')
        self.game.screen.blit(self.__background, (0, 0))
        self.game.screen.blit(self.__texto, ((self.game.largura_tela - self.__texto.get_width())//2, 186))
        self.__botoes['menu'].draw(self.game.screen)
        self.__botoes['sair'].draw(self.game.screen)
        