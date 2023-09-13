from pessoa import Pessoa


class Tecnico(Pessoa):
    def __init__(self, nome: str, codigo: int):
        super().__init__(nome, codigo)

    def __eq__(self, outro: object) -> bool:
        if isinstance(outro, Tecnico):
            return outro.codigo == self.codigo
        else:
            return False
