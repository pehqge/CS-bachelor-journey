from DAO import DAO
from Cliente import Cliente

class ClienteDAO(DAO):
    def __init__(self):
        super().__init__('clientes.pkl')
    
    def add(self, cliente: Cliente):
        if isinstance(cliente, Cliente) and isinstance(cliente.codigo, int):
            super().add(cliente.codigo, cliente)
    
    def get(self, codigo: int):
        if isinstance(codigo, int):
            return super().get(codigo)
        
    def remove(self, codigo: int):
        if isinstance(codigo, int):
            return super().remove(codigo)

    def busca_nome(self, nome: str):
        for chave, cliente in super().get_all():
            if cliente.nome == nome:
                return chave
        raise KeyError