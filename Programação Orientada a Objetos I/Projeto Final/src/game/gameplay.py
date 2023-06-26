from src.configs import SCREEN, WIDTH, Var, background
from src.assets import coracao, coracao_dead, mesa, setav_d, setav_l, setav_u, setav_r, timerbox, fonte_score, mini_high, fonte_mini_high
from src.tools import meio
from pygame import key, time, K_LEFT, K_RIGHT, K_UP, K_DOWN, K_a, K_s, K_d, K_w, mixer
from src.entities.seta import Seta
from src.entities.botao import b_sair
from src.entities.xicara import xicara_gameplay

def gameplay():
    # inicializador de musica
    if Var.playing_music or Var.playing_dead or Var.playing_high:
        mixer.music.fadeout(200)
        mixer.music.set_volume(0.3)
        Var.playing_music = False
        Var.playing_dead = False
        Var.playing_high = False
        
    if not Var.playing_gameplay_music:
        mixer.music.load("assets/gameplay.wav")
        mixer.music.play(-1)
        mixer.music.set_volume(0.2)
        Var.playing_gameplay_music = True
        
    # contador do tempo para alterar as velocidades
    Var.tempo += 0.0001
    if Var.tempo >= 2:
        Var.tempo = 2
        
    # esteticas
    background()
    SCREEN.blit(mesa, (0, 418))
    
    # xicara do gameplay
    xicara_gameplay.draw()
    b_sair.draw()
    
    # coracoes
    draw_coracoes(Var.cor_mortos)
        
    # setas
    keys = key.get_pressed() #lista booleana com as teclas pressionadas
    if keys[K_LEFT] or keys[K_a]: #seta esquerda
        setav_l.set_alpha(255) #quando pressionada, deixa ela 100% opacidade
        xicara_gameplay.angulo = max(xicara_gameplay.angulo - 4, 0) #altera o angulo da colher mexendo
        xicara_gameplay.cx = max(xicara_gameplay.cx - 4, 70) #mexe a colher pra esquerda
    else:
        setav_l.set_alpha(168) #volta pro estado da seta de 66% de opacidade
    if keys[K_RIGHT] or keys[K_d]:
        xicara_gameplay.angulo = min(xicara_gameplay.angulo + 4, 65)
        xicara_gameplay.cx = min(xicara_gameplay.cx + 4, 110)
        setav_r.set_alpha(255)
    else:
        setav_r.set_alpha(168)
    if keys[K_UP] or keys[K_w]:
        xicara_gameplay.cy = max(xicara_gameplay.cy - 2, 260)
        setav_u.set_alpha(255)
    else:
        setav_u.set_alpha(168)
    if keys[K_DOWN] or keys[K_s]:
        xicara_gameplay.cy = min(xicara_gameplay.cy + 2, 300)
        setav_d.set_alpha(255)
    else:
        setav_d.set_alpha(168) 

    # Desenha as setas gabarito na tela
    SCREEN.blit(setav_l, (30.5, 180))
    SCREEN.blit(setav_r, (258, 180))
    SCREEN.blit(setav_u, (120, 170))
    SCREEN.blit(setav_d, (188, 170))
    
    # contador de score
    if Var.game_state == Var.state_gameplay and Var.timer is None: #atribui o tempo atual para o timer
        Var.timer = time.get_ticks()
    # estetica da caixa do timer
    SCREEN.blit(timerbox, (meio(timerbox), 513))
    SCREEN.blit(mini_high, (233, 500))
    
    global timer_str, segundos #global para acessar fora da funcao dentro do mesmo arquivo
    if Var.timer is not None: 
        # inicializacao da contagem de tempo
        tempo_passado = time.get_ticks() - Var.timer 
        minutos = int(tempo_passado / 60000)
        segundos = int((tempo_passado % 60000) / 1000)
        timer_str = f"{minutos}:{segundos:02d}"
        # estetica do tempo
        timer_text = fonte_score.render(timer_str, True, "#454653")
        timer_rect = timer_text.get_rect(center=(WIDTH//2, 575))
        SCREEN.blit(timer_text, timer_rect)
        ministr = f"best {Var.score_max}" #highscore pequeno em cima do score normal
        if Var.score_max < timer_str: #chegou no highscore enquanto joga
            ministr = "HIGH SCORE"
        # estetica do mini highscore
        minihigh_text = fonte_mini_high.render(ministr, True, "#fefefe")
        minihigh_rect = minihigh_text.get_rect(center=(288.8, 518))
        SCREEN.blit(minihigh_text, minihigh_rect)

    if segundos >= 1: #inicia as setas só após 1 segundo de jogo
        Var.contador += 1 #contador de frames para controlar o tempo de spawn entre setas
        if Var.contador >= 55//Var.tempo: #quanto maior o tempo, menor o tempo de spawn
            Seta.lista_setas[Var.idx] = Seta(Var.idx) #cria uma nova seta na lista
            Var.idx += 1 #soma o id unico (fiz isso para elas ficarem na mesma posicao na lista)
            if Var.idx == 16:
                Var.idx = 0
            Var.contador = 0
        
    
    for seta in [x for x in Seta.lista_setas if x != None]: #nao conta as posicoes None
        seta.y += seta.velocidade #anima a velocidade
        seta.draw()
        if seta.verificador: #declaracao dada no arquivo main.py com as teclas apertadas
            seta.win()
        if seta.y > 220: #computador de erro
            seta.lose()
            mata()            
    
def draw_coracoes(num_mortos): #gerenciador das vidas
    for i in range(3):
        if i < 3 - num_mortos:
            SCREEN.blit(coracao, (245 + 35 * i, 314))
        else:
            SCREEN.blit(coracao_dead, (245 + 35 * i, 314))

def mata(): #reseta variaveis caso tenha feito 3 erros
    global timer_str
    if Var.cor_mortos == 3:
        Var.score = timer_str
        Var.idx = 0
        Var.contador = 0
        Var.game_state = Var.state_gameover