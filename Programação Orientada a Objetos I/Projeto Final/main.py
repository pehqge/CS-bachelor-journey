import pygame
# para iniciar o display do pygame
from src.configs import *
# entities
from src.entities.botao import b_iniciar, b_creditos, b_voltar, b_denovo, b_sair, b_menu
from src.entities.seta import Seta
# estados de jogo
from src.game.gameplay import gameplay
from src.game.menu import menu
from src.game.creditos import creditos
from src.game.gameover import gameover
    
# atualizador de frames
def update_game_display():
    pygame.display.update()
    FramePerSec.tick(FPS)
    
# cria uma lista das setas ativas de um tipo específico delas
def lista_conf(tipo):    
    return [x for x in Seta.lista_setas if x != None and x.tipo == tipo]

def main(): #funcao principal do jogo
    while True:
        # estado do menu principal
        while Var.game_state == Var.state_menu:
            for event in pygame.event.get(): #descobre se vai fechar
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP: #verifica se botões foram clicados
                    b_iniciar.handle_event(event)
                    b_creditos.handle_event(event)
            update_game_display()
            menu()
            
        # estado de créditos
        while Var.game_state == Var.state_creditos:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                    b_voltar.handle_event(event)
            update_game_display()
            creditos()
                
        # estado de gameplay
        while Var.game_state == Var.state_gameplay: 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP: #verifica botão de sair
                    b_sair.handle_event(event, True)
                    
                # verificador de cliques das setas
                elif event.type == pygame.KEYDOWN: 
                    if event.key in [pygame.K_LEFT, pygame.K_a]: #esquerda (tipo 0)
                        for seta in lista_conf(0):
                            if seta.clique():
                                seta.verificador = True #variavel interna para ativar a funcao win() da seta
                    if event.key in [pygame.K_UP, pygame.K_w]: #cima (tipo 1)
                        for seta in lista_conf(1):
                            if seta.clique():
                                seta.verificador = True
                    if event.key in [pygame.K_DOWN, pygame.K_s]: #baixo (tipo 2)
                        for seta in lista_conf(2):
                            if seta.clique():
                                seta.verificador = True
                    if event.key in [pygame.K_RIGHT, pygame.K_d]: #direita (tipo 3)
                        for seta in lista_conf(3):
                            if seta.clique():
                                seta.verificador = True
                    
            gameplay()
            update_game_display()
            
            
        # estado de gameover
        while Var.game_state == Var.state_gameover:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                    b_menu.handle_event(event, True)
                    b_denovo.handle_event(event, True)
            update_game_display()
            gameover()
                
if __name__ == "__main__":
    main()
    