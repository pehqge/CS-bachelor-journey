class ItemAbstrato:
    def __init__(self, imagem: str, som_interacao: str):
        self.__imagem = imagem
        self.__som_interacao = som_interacao
        
    @property
    def imagem(self):
        return self.__imagem
    
    @property
    def som_interacao(self):
        return self.__som_interacao

    def desaparecer_do_cenario(self):
        pass
    
    def colisao_jogador(self):
        pass

    def draw(self):
        pass