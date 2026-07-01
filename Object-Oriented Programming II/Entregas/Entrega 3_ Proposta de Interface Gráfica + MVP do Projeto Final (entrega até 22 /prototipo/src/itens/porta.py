import pygame

class Porta(pygame.sprite.Sprite):
    def __init__(self, posicao):
        super().__init__()
        self.image = pygame.image.load('Assets/im_porta.png')
        self.image.convert_alpha() #alpha porque a imagem é transparente
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(topleft = posicao)
        
    #def entrar(self, comando): #comando checa se tem ou nao a chave
        #if comando == True:
