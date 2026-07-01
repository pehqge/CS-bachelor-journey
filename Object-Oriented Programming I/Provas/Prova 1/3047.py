# neste, fiz a operação matemática de isolar uma variável, no caso "outro", para achar a idade do outro filho. Em seguida, como ele pede para imprimir a idade do filho mais velho, acho pela função "max()" e a imprimo.
m = int(input())
a = int(input())
b = int(input())
outro = m-a-b
print(max(a, b, outro))