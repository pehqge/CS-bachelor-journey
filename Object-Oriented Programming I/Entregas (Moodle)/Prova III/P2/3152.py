# meu raciociocinio para esta questão foi utilizar matemática de geometria analítica, em que a área de qualquer polígono quando se tem os vértices, é o determinante da matriz sobre 2. Fiz o cálculo no papel e apliquei a fórmula aqui no programa.

a, b = map(int, input().split())
c, d = map(int, input().split())
e, f = map(int, input().split())
g, h = map(int, input().split())
A, B = map(int, input().split())
C, D = map(int, input().split()) 
E, F = map(int, input().split())
G, H = map(int, input().split())
# minusculas -> terreno A
# maiusculas -> terreno B
# determinante A
areaA = (a*d+c*f+e*h+g*b-b*c-d*e-f*g-h*a)/2
if areaA < 0:
    areaA *=-1
# determinante B
areaB = (A*D+C*F+E*H+G*B-B*C-D*E-F*G-H*A)/2
if areaB < 0:
    areaB *=-1
if areaA >= areaB:
    print("terreno A")
else:
    print("terreno B")