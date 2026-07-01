n = int(input())

cows = []

for _ in range(n):
    g, d = map(int, input().split())
    cows.append((g, d))

cows.sort(key=lambda x: -x[0])

d_max = max(d for _, d in cows)
tempos = [False] * (d_max + 1)

milk = 0

for g, d in cows:
    for t in range(d, 0, -1):
        if not tempos[t]:
            tempos[t] = True
            milk += g
            break

print(milk)