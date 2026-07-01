import pygame
import sys
from src.estados.estado import Estado
from src.estados.botao import Botao
from src.fase.mapas import Mapa

class MenuState(Estado):
    def __init__(self, game):
        super().__init__(game)
        # CARREGAMENTO DOS ASSETS DO MENU
        background = pygame.image.load('assets/backgrounds/menu.png').convert_alpha()
        self.__background = pygame.transform.scale(background, (Mapa().largura_tela, Mapa().altura_tela))
        self.__logo = pygame.image.load('assets/logo.png').convert_alpha()
        img_botao_iniciar = pygame.image.load('assets/botoes/iniciar.png').convert_alpha()
        img_botao_sair = pygame.image.load('assets/botoes/sair.png').convert_alpha()
        self.__botoes = {'iniciar': Botao((self.game.largura_tela - img_botao_iniciar.get_width())//2 , 388, img_botao_iniciar, 1), 
                         'sair': Botao((self.game.largura_tela - img_botao_sair.get_width())//2, 528, img_botao_sair, 1)}
        

    def entering(self):
        pass
            
    def exiting(self):
        pass

    def update(self, event):
        if self.__botoes['sair'].clicado():
            pygame.quit()
            sys.exit()
            
        if self.__botoes['iniciar'].clicado():
            self.game.define_estado('jogo')
                
    def render(self):
        self.game.screen.fill('White')
        self.game.screen.blit(self.__background, (0, 0))
        self.game.screen.blit(self.__logo, ((self.game.largura_tela - self.__logo.get_width())//2, 90))
        self.__botoes['iniciar'].draw(self.game.screen)
        self.__botoes['sair'].draw(self.game.screen)
        