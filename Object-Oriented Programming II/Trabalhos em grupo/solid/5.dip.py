from abc import ABC, abstractmethod, abstractproperty

"""
Dependency Inversion Principle

Dependências devem ser feitas sobre abstrações, não sobre implementações concretas 

"""

class IPlayer(ABC):
    def __init__(self, name, hp, speed):
        self.__name = name
        self.__hp = hp
        self.__speed = speed
        
    @property
    def name(self):
        return self.__name
    
    @property
    def hp(self):
        return self.__hp

    @property
    def speed(self):
        return self.__speed 
    

class Player(IPlayer):
    def __init__(self, name):
        super().__init__(name, 20, 100)
        self.stats = StatsReporter(self)   
    
    def report(self):
        self.stats.report()


class StatsReporter:
    def __init__(self, char: Player):
        self.char = char

    def report(self):
        print(f'Name: {self.char.name}')
        print(f'HP: {self.char.hp}')
        print(f'Speed: {self.char.speed}')


player1 = Player("Pedro")
player1.report()