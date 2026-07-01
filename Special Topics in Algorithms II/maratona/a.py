n = int(input())

pontos = []

for i in range(n):
    a, b = map(int, input().split())
    pontos.append((a, b))

pontos.append(pontos[0])
    
# calcula determinante
def det(p1, p2):
    return p1[0] * p2[1] - p1[1] * p2[0]

# calcula area
area = 0
for i in range(n):
    area += det(pontos[i], pontos[i + 1])

print(abs(area))