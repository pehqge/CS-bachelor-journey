class ElevadorJahNoUltimoAndarException(Exception):
    def __init__(self):
        super().__init__("O elevador já está no último andar!")
