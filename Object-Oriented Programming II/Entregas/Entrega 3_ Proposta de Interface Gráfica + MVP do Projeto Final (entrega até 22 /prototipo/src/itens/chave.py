import pygame

class Chave(pygame.sprite.Sprite):
    def __init__(self, posicao):
        super().__init__()
        self.image = pygame.image.load('Assets/im_chave.png')
        self.image.convert()
        self.image = pygame.transform.scale(self.image, (42, 42))
        self.rect = self.image.get_rect(topleft = posicao)