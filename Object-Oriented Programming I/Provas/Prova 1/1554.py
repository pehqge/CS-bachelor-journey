c = int(input())
for _ in range(c): #for para executar c testes
  n = int(input())
  outrasx = [] #criei uma lista para armazenar os valores x de cada bola e outra lista para armazenar so os y
  outrasy = [] 
  distanciamaior = 5041000 #numero calculado pela equacao da distancia d^2=(x-xo)^2+(y-yo)^2, em que x,y = 0 e xo = 1420 e yo = 2840 (maiores valores que o input pode receber)
  contador = 0 #para utilizar posteriormente no numero da bola com menor distancia
  for i in range(0, n+1): #for para cada teste 
    x, y = map(int, input().split())
    if i == 0: #se for a primeira linha, ele armazena as variaveis para brancas
      brancax = x
      brancay = y
    else: #caso contrario, ele armazena nas listas
      outrasx.append(x)
      outrasy.append(y)
  for i in range(n): #aqui realizo o cálculo da distancia entre a bola branca e a bola de bilhar da linha n, dado pela equacao de distancias da geometria analitica
    distanciax = (brancax-outrasx[i])**2
    distanciay = (brancay-outrasy[i])**2
    distancia = (distanciax+distanciay)**(1/2)
    if distancia < distanciamaior: #se a distancia dada for menor que a "distanciamaior", ele armazena ela armazena ela para comparacoes futuras e marca no contador o numero da bola que ele esta (que é o numero da linha + 1)
      distanciamaior = distancia
      contador = i+1
  print(contador) #imprime o numero da bola
 