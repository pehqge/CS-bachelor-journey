# nessa eu apenas pego o primeiro numero em formato de string e peço apenas do ultimo elemento até o tamanho de b, para que a fique exatamente do tamanho de b
# nisso se essa versao reduzida de a for exatamente igual a b, eu imprimo "encaixa", caso ao contrario, "nao encaixa".

n = int(input())
for i in range(n):
  a, b = input().split()
  if a[-len(b):] == b:
    print("encaixa")
  else:
    print("nao encaixa")