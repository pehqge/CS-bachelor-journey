n = int(input())

def cel(f):
    return abs(5*(f)/9)

for i in range(n):
    a, b = map(int, input().split())
    print(f"Case {i+1}: {a + cel(b):.2f}")