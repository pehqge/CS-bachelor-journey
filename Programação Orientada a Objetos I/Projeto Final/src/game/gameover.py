from src.configs import background, SCREEN, WIDTH, Var
from src.assets import mesa, game_over, timerbox, fonte_score, highscore_star
from src.tools import meio, set_highscore
from src.entities.xicara import xicara_gameplay
from src.game.gameplay import draw_coracoes
from src.entities.botao import b_menu, b_denovo
from pygame import mixer

def gameover():
    # para a música atual
    if Var.playing_gameplay_music:
        mixer.music.fadeout(200)
        Var.playing_gameplay_music = False
    
    Var.tempo = 1 #reinicia o contador de tempo para velocidade
    Var.contador = 0 #reinicia o contador de frames
    background()
    # estetica
    SCREEN.blit(mesa, (0, 418))
    SCREEN.blit(game_over, (meio(game_over), 53))
    
    # computa o score e se foi highscore
    SCREEN.blit(timerbox, (meio(timerbox), 131))
    score_text = fonte_score.render(Var.score, True, "#454653")
    score_rect = score_text.get_rect(center=(WIDTH//2, 195))
    SCREEN.blit(score_text, score_rect)
    if Var.score > Var.score_max:
        Var.highs = True
        Var.score_max = Var.score
        set_highscore(Var.score)
    if Var.highs: #se for, mostra as estrelas e a mensagem
        SCREEN.blit(highscore_star, (191.86, 201.52))
      
    #controlador da musica
    if not Var.playing_high and Var.highs:  
        mixer.music.load("assets/high.wav")
        mixer.music.play(-1)
        mixer.music.set_volume(0.1)
        Var.playing_high = True
        
    if not Var.playing_dead and not Var.highs:
        mixer.music.load("assets/gameover.wav")
        mixer.music.play(-1)
        mixer.music.set_volume(0.1)
        Var.playing_dead = True

    # inicia a xicara e os botoes
    xicara_gameplay.draw()
    draw_coracoes(Var.cor_mortos)
    b_menu.draw()
    b_denovo.draw()