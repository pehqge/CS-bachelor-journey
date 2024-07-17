class Vetor:
    def __init__(self, lista):
      self.lista = lista

    def soma(self, vetor2):
      tamanho = len(self.lista)
      if tamanho != len(vetor2.lista):
        print("Não é possível fazer com este, tente com outro")
      else:
        return [self.lista[i]+vetor2.lista[i] for i in range(tamanho)]
      
    def produto_escalar(self, vetor2):
      resultado = []
      if len(self.lista) != len(vetor2.lista):
        print("Não é possível fazer com este, tente com outro")
      else:
        for i in range(len(self.lista)):
          resultado.append(self.lista[i] * vetor2.lista[1])
        return resultado
        
    def prod_inteiro(self, numero):
      return [i*numero for i in self.lista]

vetor1 = Vetor([4, 5, 6])
print(vetor1.lista)
print(vetor1.prod_inteiro(4))
print(type("oi"))
lista = [2, 4, 5]
lista.remove