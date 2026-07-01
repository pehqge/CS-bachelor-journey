from abc import ABC
import pickle

class DAO(ABC):
    def __init__(self, arquivo = ""):
        self.__arquivo = arquivo
        self.__cache = {}
        try:
            self.__load()
        except FileNotFoundError:
            self.__dump()
            
    @property
    def cache(self):
        return self.__cache
        
    def __dump(self):
        f = open(self.__arquivo, 'wb')
        pickle.dump(self.__cache, f)
        f.close()
        
    def __load(self):
        f = open(self.__arquivo, 'rb')
        self.__cache = pickle.load(f)
        f.close()
        
    def add(self, chave, obj):
        self.__cache[chave] = obj
        self.__dump()
        
    def get(self, chave):
        try:
            return self.__cache[chave]
        except KeyError:
            print("Chave não encontrada")
            raise KeyError
        
    def remove(self, chave):
        try:
            self.__cache.pop(chave)
            self.__dump()
        except KeyError:
            raise KeyError
        
    def get_all(self):
        return self.__cache.items()