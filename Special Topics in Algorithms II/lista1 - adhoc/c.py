n = int(input())

deck = [1,2,3,4,5,6,7,8,9,10,11,12,13]*4


j = [int(i) for i in input().split()]
m = [int(i) for i in input().split()]
common = [int(i) for i in input().split()]

for i in range(2):
    deck.remove(j[i])
    deck.remove(m[i])
    
    if j[i] in [11,12,13]:
        j[i] = 10
    if m[i] in [11,12,13]:
        m[i] = 10
    
for i in range(n):
    deck.remove(common[i])
    if common[i] in [11,12,13]:
        common[i] = 10

    
sC = sum(common)
sJ = sum(j) + sC
sM = sum(m) + sC


if sJ > sM:
    vence = 24-sJ
else:
    vence = 23 - sM
    
    
while not vence in deck or vence > 10:
    vence += 1
    if vence + sM >= 24 or vence > 10:
        vence = -1
        break

print(vence)