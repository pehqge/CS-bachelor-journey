class Amigo:
    def __init__(self,
                 nome: str,
                 telefone: list,
                 email: str):
        if isinstance(nome, str):
            self.__nome = nome
        if (isinstance(telefone, list)
            and len(telefone) > 0
                and all(isinstance(x, str) for x in telefone)):
            self.__telefone = telefone
        if isinstance(email, str):
            self.__email = email

    @property
    def nome(self):
        return self.__nome

    @property
    def telefone(self):
        return self.__telefone

    @property
    def email(self):
        return self.__email
