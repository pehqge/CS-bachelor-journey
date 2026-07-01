import math

n = int(input())

for i in range(n):
    a, b, c = map(int, input().split())
    print(f"Case {i + 1}: ", end="")
    if c % math.gcd(a, b) == 0:
        print("Yes")
    else:
        print("No")