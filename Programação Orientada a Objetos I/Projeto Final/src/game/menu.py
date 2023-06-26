from src.configs import background, WIDTH, SCREEN, Var
from src.assets import fonte_scoremax, logo, mesa, cara_main
from src.tools import seno
from src.entities.xicara import Xicara
from src.entities.botao import b_iniciar, b_creditos
from pygame import mixer



def menu():
    Var.tempo = 1 #reinicia o contador de tempo
    
    # inicializador de musica
    if Var.playing_gameplay_music or Var.playing_dead or Var.playing_high:
        mixer.music.fadeout(200)
        Var.playing_gameplay_music = False
        Var.playing_dead = False
        Var.playing_high = False
    if not Var.playing_music:
        mixer.music.load("assets/menu.wav")
        mixer.music.play(-1)
        mixer.music.set_volume(0.3)
        Var.playing_music = True
    
    background()
    
    # marcador do highscore no topo
    best_score = fonte_scoremax.render("best score   " + str(Var.score_max), True, "#F38489")
    best_score_rect = best_score.get_rect(center=(WIDTH//2, 40))
    SCREEN.blit(best_score, best_score_rect)
    
    # logo mexendo
    y = seno(200.0, 1280, 6.0, 60)
    SCREEN.blit(logo, (-17, y))
    
    SCREEN.blit(mesa, (0, 358))
    
    # xicara do menu
    xicara_menu = Xicara(58, 281, cara_main)
    xicara_menu.draw()
    
    # botoes
    b_iniciar.draw()
    b_creditos.draw()
    