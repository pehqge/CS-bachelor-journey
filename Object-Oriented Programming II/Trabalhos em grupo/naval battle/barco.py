from random import randint

class Barcos:
    def __init__(self, listaaux=[], contador=0):
        self.meus_barcos={}
        self.contador = contador
        self.listaaux = listaaux

# metodo para ser utilizado quando o jogador precisar escolher o barco na hora inicial
    def escolha_jogador(self,numero_barco): 
        if self.meus_barcos == {}:
            posicao = input('Escolha a posicao que deseja adicionar o barco da forma "A4", com linhas de A ate J e colunas de 1 a 10: ').upper()
        else:
            posicao = input('Agora escolha outra posição na forma A4: ').upper()
        if posicao in self.meus_barcos: #verifica se a posicao ja existeaa
            print(f'Você já tem um barco nessa posição, escolha novamente!')
            self.escolha_jogador(numero_barco) #roda o metodo novamente
        else:
            self.meus_barcos[posicao]= f'barco {numero_barco}' #add o barco no dicionario
            
    def escolha_computador(self): #metodo que escolhe as posicoes dos barcos da maquina
        letras=['A','B','C','D','E','F','G','H','I','J']
        numero= randint(1,10)
        escolha_letra=randint(0,9) 
        return letras[escolha_letra]+str(numero) 
    
    def gerador_ai(self):
        gerado = self.escolha_computador()
        if not gerado in self.meus_barcos:
            self.meus_barcos[gerado] = f"barco {len(self.meus_barcos)+1}"  #adiciona o barco
        if len(self.meus_barcos) != 8: #Numero maximo de barcos da maquina = 8
            self.gerador_ai()
    
    def jogador_ataque(self,barcos_inimigos):
      if self.contador == 8:
        print('Você ganhou!')
      else:
        posicao = input('Escolha a posicao que deseja atacar a bomba, na forma "A4", com linhas de A ate J e colunas de 1 a 10: ').upper()
        if posicao not in self.listaaux:
          self.listaaux.append(posicao)
          if posicao in barcos_inimigos: #verifica se há um barco da maquina na posicao escolhida
            self.contador += 1
            print(f'Você acertou o {barcos_inimigos[posicao]} na posição {posicao}!')
            self.jogador_ataque(barcos_inimigos) #roda o metodo novamente
          else:
              print(f'Você errou!')
        else:
            print(f'Você já marcou essa posição! Tente novamente!')
            self.jogador_ataque(barcos_inimigos)
            
    
    def maquina_ataque(self, barcos_jogador):
        if self.contador == 8:
          print('O computador ganhou!')
        else:
            print("Vez do computador")
            posicao = self.escolha_computador()
            if posicao not in self.listaaux:
                self.listaaux.append(posicao)
                if posicao in barcos_jogador:
                    self.contador += 1
                    print(f'Computador acertou o {barcos_jogador[posicao]} na posição {posicao}!')
                    self.maquina_ataque(barcos_jogador)
                else:
                    print(f'Computador errou!')
            else:
                self.maquina_ataque(barcos_jogador)
                
        
        
    
        
        
        