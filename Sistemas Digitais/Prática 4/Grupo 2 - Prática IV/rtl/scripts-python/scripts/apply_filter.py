def monta_kernel(matriz_kernel):
    kernel = [bin(pixel)[2:].zfill(8) for linha in matriz_kernel for pixel in linha]
    with open('kernel.txt', 'w') as file:
        file.write("\n".join(kernel))

def filtro_pixel(matriz_file, kernel_file):
    mem = [] # matriz que vai receber arquivo
    kernel = [] # kernel que vai receber arquivo
    
    # leituras de arquivos
    with open(matriz_file, 'r') as file:
        for linha in file:
            mem.append(int(linha, 2))

    with open(kernel_file, 'r') as file:
        for linha in file:
            kernel.append(int(linha, 2))

    mem_saida = ['255']*(600*600) # matriz final, inicializada toda branca

    linha = 1 # começa em 1 pois precisa desconsiderar a primeira linha
    pronto = 0 # flag para o vhdl

    # percorre a matriz (imagem)
    while linha < 601:
        coluna = 1 # reseta a coluna para cada linha
        while coluna < 601:
            soma = 0 # resultado
            i = 0 # indice da matriz 3x3 do kernel
            
            # variaveis para formar a matriz 3x3 da imagem
            deslocaLinha = -1
            deslocaColuna = -1
            
            # percorre a matriz 3x3
            while i < 9:
                # seleção do pixel com o kernel para a convolução
                k = kernel[i] 
                m = mem[(linha + deslocaLinha)*602 + (coluna + deslocaColuna)] 
                
                res = k*m # multiplicação da "convolução parcial"
                res = bin(res)[2: len(res)].zfill(8) # transforma em binário
                resb = res[0:len(res)-4].zfill(8) # divide por 16 em bin
                resi = int(resb, 2) # transforma em inteiro
                
                soma += resi # soma o resultado da "convolução parcial"
                
                # atualização das variaveis
                i += 1
                deslocaColuna += 1

                # se a coluna for 3, desloca para a proxima linha
                if deslocaColuna > 1:
                    deslocaColuna = -1
                    deslocaLinha += 1
                    
            soma = bin(soma) # resultado final da convolução
            soma = soma[2:len(soma)].zfill(8)
            mem_saida[(linha-1)*600 + (coluna-1)] = soma # atualiza a matriz final (imagem)
            
# atualização das variaveis
            coluna += 1
        linha += 1
    pronto = 1
    
    # escreve a matriz final no arquivo matriz_filtrada.txt
    with open('matriz/matriz_filtrada.txt', 'w') as arquivo:
        arquivo.write("\n".join(mem_saida))
    