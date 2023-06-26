import random
from src.entities.xicara import xicara_gameplay
from pygame import image
from src.configs import SCREEN, Var

class Seta:
    lista_setas = [None for i in range(16)]
    lista_tipos = []
    def __init__(self, idx):
        self.idx = idx #id da seta
        self.velocidade = 1.5**Var.tempo #velocidade variavel
        self.opacidade = 255 #opacidade da seta para caso perder
        self.eopacidade = 0 #opacidade do X erro
        self.y = -60
        self.ye = 183 #y do X erro
        self.tipo = self.gerar_tipo() #o tipo de 0 a 3 representa a orientacao da seta
        if self.tipo == 0: #esquerda
            self.x = 30.5
            self.xe = 48
            self.ya = 155 #y do acerto
            self.xa = 51 #x do acerto
            self.img = image.load("assets/seta_l.png").convert_alpha()
        elif self.tipo == 1: #cima
            self.x = 120
            self.xe = 122
            self.ya = 188
            self.xa = 134
            self.img = image.load("assets/seta_u.png").convert_alpha()
        elif self.tipo == 2: #baixo
            self.x = 188
            self.xe = 192
            self.ya = 188
            self.xa = 203
            self.img = image.load("assets/seta_d.png").convert_alpha()
        elif self.tipo == 3: #direita
            self.x = 258
            self.xe = 264
            self.ya = 155
            self.xa = 300
            self.img = image.load("assets/seta_r.png").convert_alpha()
        self.error = image.load("assets/missed.png").convert_alpha()
        self.acerto = image.load("assets/acerto.png").convert_alpha()
        self.contador = 0 #conta frames para animacoes
        self.mata = None #var para alterar valor de vida e cara da xicara, unica vez
        self.verificador = False #verifica se a seta foi acertada
        
    def draw(self):
        SCREEN.blit(self.img, (self.x, self.y))
        
    def lose(self): #quando perde
        if self.mata is None: #atualiza os valores uma unica vez
            Var.cor_mortos += 1
            xicara_gameplay.update_face(Var.cor_mortos)
            self.mata = 1
        self.opacidade -= 40 #diminui a opacidade para sumir da tela
        self.img.set_alpha(self.opacidade)
        self.contador += 1
        # aparece o X do erro
        if self.contador <= 12: #aparece
            self.error.set_alpha(self.eopacidade)
            self.eopacidade += 30.5
            SCREEN.blit(self.error, (self.xe, self.ye))
        elif self.contador <= 35: #permanece
            SCREEN.blit(self.error, (self.xe, self.ye))
        elif self.contador <= 48: #some
            self.eopacidade -= 21.5
            self.error.set_alpha(self.eopacidade)
            SCREEN.blit(self.error, (self.xe, self.ye))
        else: #depois do X sumir, ela remove da lista
            Seta.lista_setas[self.idx] = None
            Seta.lista_tipos.remove(self.tipo)
                
    def win(self): #quando ganha
        self.contador += 1
        self.y = -200
        if self.contador <= 12:
            self.acerto.set_alpha(self.eopacidade)
            self.eopacidade += 30.5
            SCREEN.blit(self.acerto, (self.xa, self.ya))
        elif self.contador <= 35:
            SCREEN.blit(self.acerto, (self.xa, self.ya))
        elif self.contador <= 48:
            self.eopacidade -= 21.5
            self.acerto.set_alpha(self.eopacidade)
            SCREEN.blit(self.acerto, (self.xa, self.ya))
        else:
            Seta.lista_setas[self.idx] = None
            Seta.lista_tipos.remove(self.tipo)
                
    def gerar_tipo(self): #verifica se n esta gerando o mesmo tipos dos ultimos 2
        tipo = random.randint(0, 3)
        if len(Seta.lista_setas) > 0:
            while tipo in Seta.lista_tipos[-2:]:
                tipo = random.randint(0, 3)
        Seta.lista_tipos.append(tipo)
        return tipo
    
    def clique(self): #verificador do gabarito da seta
        if self.tipo in [0, 3]:
            if self.y >= 145 and self.y <= 208:
                return True
        elif self.tipo in [1, 2]:
            if self.y >= 130 and self.y <= 200:
                return True
        return False
    
