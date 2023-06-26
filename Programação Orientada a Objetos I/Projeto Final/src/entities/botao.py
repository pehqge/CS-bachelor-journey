from pygame import Rect, mouse, MOUSEBUTTONDOWN, MOUSEBUTTONUP
from src.assets import iniciar, iniciar_f, bcreditos, bcreditos_f, voltar, voltar_f, sair, sair_f, b_menu, b_menu_f, denovo, denovo_f, som_botao
from src.configs import SCREEN, Var
from src.tools import meio
from src.entities.seta import Seta
from src.entities.xicara import xicara_gameplay


class Botao:
    def __init__(self, nome, nome_f, x, y, estado, fx=10, fy=7):
        self.nome = nome #imagem da frente
        self.nome_f = nome_f #imagem da sombra
        self.x = x
        self.y = y
        self.fx = fx #posicao da sombra
        self.fy = fy
        self.estado = estado #para qual estado que deve mudar
        self.pressed = False

    def draw(self):
        rect = Rect(self.x, self.y, self.nome.get_width(), self.nome.get_height())
        if rect.collidepoint(mouse.get_pos()): #animacao se passar o mouse por cima
            pos_texto = (self.x + self.fx/3, self.y + self.fy/7)
            if self.pressed: #animacao quando apertado
                pos_texto = (self.x + self.fx, self.y + self.fy)
        else:
            self.pressed = False
            pos_texto = (self.x, self.y)

        SCREEN.blit(self.nome_f, (self.x + self.fx, self.y + self.fy))
        SCREEN.blit(self.nome, pos_texto)
    
    def handle_event(self, event, Bool=False): #muda de estado se for apertado
        rect = Rect(self.x, self.y, self.nome.get_width(), self.nome.get_height())
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if rect.collidepoint(mouse.get_pos()):
                    self.pressed = True
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                if rect.collidepoint(mouse.get_pos()):
                    if self.pressed:
                        if Bool: #booleana para saber se o botão reseta tudo se for apertado
                            Var.cor_mortos = 0
                            xicara_gameplay.update_face(0)
                            xicara_gameplay.angulo = 0
                            Var.timer = None
                            Var.highs = False
                            xicara_gameplay.cx = 119
                            xicara_gameplay.cy = 300
                            Seta.lista_setas = [None for i in range(16)]
                            Seta.lista_tipos = []
                            Var.idx = 0
                            Var.tempo = 1
                            Var.contador = 0
                        som_botao.set_volume(0.5)
                        som_botao.play()
                        Var.game_state = self.estado
                    self.pressed = False

# definindo botoes
b_iniciar = Botao(iniciar, iniciar_f, 97, 457, Var.state_gameplay)
b_creditos = Botao(bcreditos, bcreditos_f, 77, 540, Var.state_creditos)
b_voltar = Botao(voltar, voltar_f, meio(voltar), 400, Var.state_menu)
b_sair = Botao(sair, sair_f, 314, 11, Var.state_menu, 6, 4)
b_menu = Botao(b_menu, b_menu_f, 196.79, 564, Var.state_menu)
b_denovo = Botao(denovo, denovo_f, 185, 501, Var.state_gameplay)