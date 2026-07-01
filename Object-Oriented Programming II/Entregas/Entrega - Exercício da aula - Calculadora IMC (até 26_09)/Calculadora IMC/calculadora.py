class CalculadoraIMC:
    def __init__(self, peso, altura):
        self.__peso = peso
        self.__altura = altura
        
    @property
    def peso(self):
        return self.__peso
    
    @property
    def altura(self):
        return self.__altura
    
    def calcular(self):
        imc = self.peso / (self.altura ** 2)
        return imc
        
    def tipoIMC(self, imc):
        if imc < 18.5:
            imc_tipo = "abaixo do peso"
        elif 18.5 <= imc < 24.9:
            imc_tipo = "com o peso normal"
        elif 25 <= imc < 29.9:
            imc_tipo = "sobrepeso"
        else:
            imc_tipo = "obeso"
        return imc_tipo