class HUD:
    def __init__(self, num_vidas: int, indicador_chave: bool, num_fase: int):
        self.__num_vidas = num_vidas
        self.__indicador_chave = indicador_chave
        self.__num_fase = num_fase
    
    @property
    def num_vidas(self):
        return self.__num_vidas
    
    @property
    def indicador_chave(self):
        return self.__indicador_chave
    
    @property
    def num_fase(self):
        return self.__num_fase
    
    def draw(self):
        pass