# aqui, crio um dicionario para armazenar cada runa e quanto de amizade cada uma possui
# depois, crio uma lista das runas utilizadas e vou iterando sobre cada uma e somando no total o valor armazenado no dicionario de runas
# se o total das somas for maior ou igual que o da amizade necessaria (g), eles ganharam

runas, amiz = map(int, input().split())
dic = {}
for i in range(runas):
    r, v = input().split()
    dic[r] = int(v)
x = int(input())
ru = list(input().split())
total = 0
for i in ru:
    total += dic[i]
print(total)
if total >= amiz:
    print("You shall pass!")
else:
    print("My precioooous")