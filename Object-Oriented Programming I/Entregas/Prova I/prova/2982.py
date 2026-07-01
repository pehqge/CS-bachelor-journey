#neste problema, criei 2 listas vazias para conseguir organizar os dados que o input oferece: uma de gastos e outra para a de valores. Nisso, crio um for para receber os inputs determinados pelo n, e ao fazer isso, utilizo das letras "G" e "V" para colocar nas listas cada valor de gastos e valores do governo, respectivamente. No final, somo todos os valores de cada lista e comparo para ver qual é maior. Se o gasto for maior que o valor, a greve continua, caso ao contrário, a greve para.
n = int(input())
gastos = []
valores = []
for _ in range(n):
  c, t = map(str, input().split())
  t = int(t)
  if c == "G":
    gastos.append(t)
  else:
    valores.append(t)
gasto = sum(gastos)
valor = sum(valores)
if gasto>valor:
  print("NAO VAI TER CORTE, VAI TER LUTA!")
else:
  print("A greve vai parar.")