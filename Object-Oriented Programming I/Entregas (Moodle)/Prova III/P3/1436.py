# nesse eu só procuro pelo item que está exatamente no meio da lista quando a organizo de menor para maiores e o imprimo


n = int(input())
for i in range(n):
  lista = list(map(int, input().split()))
  lista.sort()
  print(f"Case {i+1}: {lista[len(lista)//2]}")