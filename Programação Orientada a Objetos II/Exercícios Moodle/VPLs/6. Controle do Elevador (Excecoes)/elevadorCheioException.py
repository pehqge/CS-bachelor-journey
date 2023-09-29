class ElevadorCheioException(Exception):
    def __init__(self):
        super().__init__("O elevador esta cheio!")
