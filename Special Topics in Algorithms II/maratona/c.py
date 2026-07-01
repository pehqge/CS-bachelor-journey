n, c = map(int, input().split())
s = list(map(int, input().split()))

max_subseq = 0

subseq = 0

for i in range(1, n):
    if s[i] != s[i - 1]:
        subseq += 1
    else:
        if subseq > max_subseq:
            max_subseq = subseq
        subseq = 0
        
print(max_subseq + 1)