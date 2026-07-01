import pygame

class Jogador(pygame.sprite.Sprite):
    def __init__(self, posicao: tuple, velocidade: int):
        super().__init__()
        self.image = pygame.Surface((42,64)) #64x64 faria q o jogador tivesse um tile de tamanho
        self.image.fill('red')
        self.rect = self.image.get_rect(topleft = posicao)
        self.__direcao = pygame.math.Vector2(0,0)

        #movimento do jogador
        self.__velocidade = velocidade
        self.__gravidade = 0.8
        self.__altura_pulo = -15


        self.__abrir_porta = False


    @property
    def posicao(self):
        return self.__posicao
    
    def andar(self):
        teclas = pygame.key.get_pressed() #mapeia as teclas
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]: #implementa a direção em que o jogador anda
            self.__direcao.x = 1
        elif teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.__direcao.x = -1
        else:
            self.__direcao.x = 0

        #if teclas[pygame.K_UP] and self.rect.bottom == : #implementa o pulo
         #   self.pular()


    def update(self): #TEM que ter o nome de update, se não, nao vai funcionar em Fase.py por causa do pygame groups
        self.andar() 
        

    def aplicar_gravidade(self):
        self.__direcao.y += self.__gravidade
        self.rect.y += self.__direcao.y

    def pular(self):
        self.__direcao.y = self.__altura_pulo

    def agachar(self):
        pass

    def desbloquear_porta(self):
        self.__abrir_porta = True

    @property
    def abrir_porta(self):
        return self.__abrir_porta

    def chave_segue(self):
        pass

    @property
    def direcao(self):
        return self.__direcao
    
    @property
    def velocidade(self):
        return self.__velocidade
    
    @property
    def gravidade(self):
        return self.__gravidade