class ElevadorJahNoTerreoException(Exception):
    def __init__(self):
        super().__init__("O elevador já está no térreo!")
