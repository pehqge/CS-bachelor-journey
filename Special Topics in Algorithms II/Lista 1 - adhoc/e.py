n = int(input())

maximum = 0
current = 0
zero = []
one = []
stop = False

for _ in range(n):
    t, d = map(int, input().split())
    if not stop:
        current = d
        stop = True
    
    if d == 0:
        zero.append(t)
    else:
        one.append(t)

# casos:
# 1. entrou com escada parada
# 2. entrou com escada em movimento na mesma direção
# 3. teve que esperar a escada parar
candidato = 0
while n > 0:
    if current == 0:
        
        if zero == []: # se não tem ninguém esperando, muda sentido
            current = 1
            stop = True
        else:
            if stop:
                maximum = max(maximum + 10, zero[0] + 10)
                zero.pop(0)
                n-=1
                stop = False
            else:
                candidato = zero[0]
                if candidato <= maximum or (one != [] and candidato < one[0]):
                    maximum = max(candidato + 10, maximum)
                    zero.pop(0)
                    n-=1
                else:
                    current = 1
                    stop = True
    else:
        if one == []:
            current = 0
            stop = True
        else:
            if stop:
                maximum = max(maximum + 10, one[0] + 10)
                one.pop(0)
                n-=1
                stop = False
            else:
                candidato = one[0]
                if candidato <= maximum or (zero != [] and candidato < zero[0]):
                    maximum = max(candidato + 10, maximum)
                    one.pop(0)
                    n-=1
                else:
                    current = 0
                    stop = True
            
print(maximum)