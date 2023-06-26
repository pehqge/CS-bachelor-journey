from json import load, dump
from pygame import time
from math import sin
from src.configs import WIDTH, Var

# funcoes do highscore
def get_highscore(): #le o highscore do arquivo
    with open("score.json", "r") as f:
        return load(f)["best"]
def set_highscore(score): #salva o highscore
    with open("score.json", "w") as f:
        dump({"best": score}, f)
Var.score_max = get_highscore()

def meio(imagem): # alinha a imagem para o meio
    largura_imagem = imagem.get_width()
    posicao_x = (WIDTH - largura_imagem) // 2
    return posicao_x

def seno(vel, tempo, longe, Yinicial): # funcao seno para animacoes
	t = time.get_ticks() / 2 % tempo
	x = t
	y = sin(t/vel) * longe + Yinicial 
	y = int(y)
	return y
