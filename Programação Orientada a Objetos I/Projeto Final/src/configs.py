import pygame
from src.assets import bg

# Informacao do Jogo e de inicializacao
pygame.init()
WIDTH = 360
HEIGHT = 640
FPS = 90
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
SCREEN.fill("#FFD8D7")
pygame.display.set_caption("misture meu chá!")
pygame.display.set_icon(pygame.image.load("assets/icone.png"))
FramePerSec = pygame.time.Clock()

    
# Inicializacao de variaveis globais
class Var:
    # codigos dos estados
    state_menu = 0
    state_creditos = 1
    state_gameplay = 2
    state_gameover = 3
    game_state = state_menu
    
    scroll = -83 # velocidade do scroll do bg
    timer = None #controla o timer do gameplay
    highs = False #verifica se o highscore foi atingido
    cor_mortos = 0 #numero de coracoes mortos
    contador = 0 #contador de frames para gameplay
    score = '' #score atual
    score_max = '' #highscore
    tempo = 1 #tempo para usar no controle da velocidade
    idx = 0 #id unico para as setas
    playing_music = False #musica menu
    playing_gameplay_music = False #musica gameplay
    playing_high = False #musica quando faz highscore
    playing_dead = False #musica quando morre


# incializacao do background
def background():
    Var.scroll += .5
    if Var.scroll > 0:
        Var.scroll = -83
    SCREEN.blit(bg, (0, Var.scroll))