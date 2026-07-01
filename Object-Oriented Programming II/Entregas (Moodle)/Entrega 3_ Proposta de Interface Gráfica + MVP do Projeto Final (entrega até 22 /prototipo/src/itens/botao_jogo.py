import pygame

class Botao_Jogo(pygame.sprite.Sprite):
    def __init__(self, posicao):
        super().__init__()
        self.image = pygame.image.load('Assets/im_botao.png')
        self.image.convert()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(topleft = posicao)




    def interacao_jogador(self):
        pass