class Grupo:
    def __init__(self, nome):
        if isinstance(nome, str):
            self.__nome = nome
        else:
            raise ValueError
        self.__lista_equipe = []

    def atribuir_equipe(self, equipe):
        self.__lista_equipe.append(equipe)

    @property
    def nome(self):
        return self.__nome
    
    @property
    def lista_equipe(self):
        return self.__lista_equipe