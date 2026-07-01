from abc import ABC, abstractmethod

"""
Open-Closed Principle

Classes devem estar fechadas para modificação, mas abertas para extensão
"""


class AnimalAbstrato(ABC):
    def __init__(self, name: str):
        self.__name = name

    @property
    def name(self):
        return self.__name

    @abstractmethod
    def make_sound(self):
        pass

class Lion(AnimalAbstrato):
    def __init__(self):
        super().__init__('Lion')

    def make_sound(self):
        print('roar')

class Mouse(AnimalAbstrato):
    def __init__(self):
        super().__init__('Mouse')

    def make_sound(self):
        print('squeak')
        
class Penguin(AnimalAbstrato):
    def __init__(self):
        super().__init__('Penguin')

    def make_sound(self):
        print('quack')

def animal_sound(animals: list):
    for animal in animals:
        animal.make_sound()
        
animals = [Lion(), Mouse(), Penguin()]

animal_sound(animals)


"""
Outro exemplo:

Imagine que você tem uma loja que dá desconto de 20% aos seus clientes favoritos
usando essa classe abaixo. Quando você decide dar 40% de desconto a clientes VIP,
você decide mudar a classe da seguinte forma:
"""

class Discount:
    def __init__(self, customer, price):
        self.customer = customer
        self.price = price

    def give_discount(self):
            return f"R$ {self.price * (1 - self.customer.discount()):.02f}"
            
class ClienteAbstract(ABC):
    def __init__(self, name: str):
        self.__name = name
        
    def discount(self):
        pass
    

class ClienteFav(ClienteAbstract):
    def __init__(self, name):
        super().__init__(name)
    
    def discount(self):
        return 0.2

    
class ClienteVip(ClienteAbstract):
    def __init__(self, name):
        super().__init__(name)
    
    def discount(self):
        return 0.4
    
class ClienteRuim(ClienteAbstract):
    def __init__(self, name):
        super().__init__(name)
    
    def discount(self):
        return -0.05


def give_discount(clients: list, valor: float):
    for client in clients:
        print(Discount(client, valor).give_discount())

cliente1 = ClienteVip('Pedro')
cliente2 = ClienteFav('Augusto')
cliente3 = ClienteRuim('Tom')
clients=[cliente1,cliente2,cliente3]

give_discount(clients, 100)


