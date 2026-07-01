while True:
    n, m = map(int, input().split())
    if n == 0 and m == 0:
        break
    
    matriz = []
    
    for i in range(n):
        linha = list(map(int, input().split()))
        matriz.append(linha)
        
    # linha = competidor
    # coluna = problema
    
    # 1. Ninguém resolveu todos os problemas.
    # conferir se nao existe linha com tudo = 1
    caracteristica1 = True
    
    for competidor in matriz:
        if competidor == [1]*m:
            caracteristica1 = False
            break
        
    # 2. Todo problema foi resolvido por pelo menos uma pessoa 
    # conferir se todas as colunas sao != [0,0,0,0]
    caracteristica2 = True
    
    for coluna in range(m):
        for linha in range(n):
            if matriz[linha][coluna]:
                continue ## FAZER DEPOIS
            
    # 3. Não há nenhum problema resolvido por todos.
    # conferir se todas as colunas sao != [1, 1, 1, 1]
    
    # 4. Todos resolveram ao menos um problema 
    caracteristica4 = True
    
    for competidor in matriz:
        if competidor == [0]*m:
            caracteristica1 = False
            break
    
        
    