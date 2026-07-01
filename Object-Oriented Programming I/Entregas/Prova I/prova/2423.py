# comecei dividindo cada ingrediente pela quantidade de medidas dele para achar quantos bolos o único ingrediente consegue fazer. Para saber o total de bolos que se pode fazer é preciso achar a menor quantidade entre os 3 ingredientes, que é obtido pela função min()
f, o, l = map(int, input().split())
f //= 2
o //= 3
l //= 5
print(min(f,o,l))