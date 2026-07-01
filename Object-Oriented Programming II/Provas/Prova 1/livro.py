class Livro:
    def __init__(self, titulo: str,
                 resumo: str,
                 autor: str,
                 personagem_principal: str,
                 genero: str,
                 faixa_etaria: str):
        if isinstance(titulo, str):
            self.__titulo = titulo
        if isinstance(resumo, str):
            self.__resumo = resumo
        if isinstance(autor, str):
            self.__autor = autor
        if isinstance(personagem_principal, str):
            self.__personagem_principal = personagem_principal
        if isinstance(genero, str):
            self.__genero = genero
        if isinstance(faixa_etaria, str):
            self.__faixa_etaria = faixa_etaria

    @property
    def titulo(self):
        return self.__titulo

    @property
    def resumo(self):
        return self.__resumo

    @property
    def autor(self):
        return self.__autor

    @property
    def personagem_principal(self):
        return self.__personagem_principal

    @property
    def genero(self):
        return self.__genero

    @property
    def faixa_etaria(self):
        return self.__faixa_etaria
