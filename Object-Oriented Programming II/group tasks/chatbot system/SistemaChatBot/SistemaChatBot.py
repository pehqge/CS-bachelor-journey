import pickle

class SistemaChatBot:
    def __init__(self, nomeEmpresa, arquivo):
        self.__empresa = nomeEmpresa
        self.__arquivo = arquivo
        self.__lista_bots = []
        try:
            self.__load()
        except FileNotFoundError:
            self.__dump()
        
    @property
    def lista_bots(self):
        return self.__lista_bots
    
    @property
    def empresa(self):
        return self.__empresa
    
    def __dump(self):
        f = open(self.__arquivo, 'wb')
        pickle.dump(self.__lista_bots, f)
        f.close()
        
    def __load(self):
        f = open(self.__arquivo, 'rb')
        self.__lista_bots = pickle.load(f)
        f.close()
    
    def addbot(self, bot):                              
        if not bot in self.lista_bots:
            self.lista_bots.append(bot)
            self.__dump()
        else:
            raise ValueError("Bot já está na lista de bots")
        
    def editbot(self, bot):
        if bot in self.lista_bots:
            self.__dump()
        else:
            raise ValueError("Não é um bot válido ou não está na lista de bots")
    
    def removebot(self, bot):
        if bot in self.lista_bots:
            self.lista_bots.remove(bot)
            self.__dump()
        else:
            raise ValueError("Não é um bot válido ou não está na lista de bots")