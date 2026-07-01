#se o resto for 0 entre o valor e a parcela, ele imprime normalmente o looping com cada parcela. Já quando o resto é maior que 1, eu armazeno a quantidade do resto na variavel "resto" e depois faço um looping em que ele adiciona 1 na parcela e em seguida tira 1 do resto até o resto chegar a 0, e imprime as demais parcelas sem soma também.
valor = int(input())
parcela = int(input())
if valor%parcela == 0:
  for i in range(parcela):
    print(int(valor/parcela))
else:
  resto = valor%parcela
  for i in range(parcela):
    if resto > 0:
      total = valor//parcela + 1
      resto -= 1
      print(total)
    else:
      print(valor//parcela)