import pygame

class TileMap(pygame.sprite.Sprite):
    def __init__(self, posicao, tamanho, cor):
        super().__init__()
        self.image = pygame.Surface((tamanho,tamanho)) # valores de x e y (iguais nesse caso)
        self.image.fill(cor)
        self.rect = self.image.get_rect(topleft = posicao)