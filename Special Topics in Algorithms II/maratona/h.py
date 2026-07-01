n = int(input())
S = input()

tams_unicos = []
i = 0

while i < n:
    cor = S[i]
    count = 0
    while i < n and S[i] == cor:
        count += 1
        i += 1
    tams_unicos.append(count)
    
if len(tams_unicos) == 1:
    print(0)
    exit()

    
if len(tams_unicos) == 2:
    if tams_unicos[0] == tams_unicos[1]:
        print(tams_unicos[0]*2)
        exit()

max_l = 0

for i in range(len(tams_unicos)-1):
    if i == 0:
        if len(tams_unicos) % 2 == 0:
            max_l = min(tams_unicos[0], tams_unicos[-1]) * 2
            
        else:
            if tams_unicos[0] + tams_unicos[-1] == tams_unicos[1]:
                l = tams_unicos[1] * 2
                max_l = max(max_l, l)
    
    else:
        if tams_unicos[i] == tams_unicos[i - 1] + tams_unicos[i + 1]:
            l = tams_unicos[i] * 2
            max_l = max(max_l, l)
            
if max_l == 0:
    for i in range(len(tams_unicos)-1):
        l = min(tams_unicos[i], tams_unicos[i + 1]) * 2
        max_l = max(max_l, l)

print(max_l)