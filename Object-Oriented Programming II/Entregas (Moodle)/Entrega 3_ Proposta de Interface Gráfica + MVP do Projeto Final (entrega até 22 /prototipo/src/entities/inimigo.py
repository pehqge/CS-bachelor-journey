from typing import Any
import pygame

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, posicao, move_speed: int):
        super().__init__()
        self.image = pygame.image.load('Assets/im_inimigo.gif')
        self.image.convert_alpha()
        self.image = pygame.transform.scale(self.image, (48, 64))
        self.__velocidade = move_speed
       # self.image = pygame.Surface((42,64)) #64x64 faria q o jogador tivesse um tile de tamanho
       # self.image.fill('red')
        self.rect = self.image.get_rect(topleft = posicao)
        self.__direcao = pygame.math.Vector2((self.__velocidade),0)


    @property
    def velocidade(self):
        return self.__velocidade
    
    @property
    def direcao(self):
        return self.__direcao
    
    def virar(self):
        self.image = pygame.transform.flip(self.image, True, False)

    