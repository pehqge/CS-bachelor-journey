from PIL import Image

def img_to_matrix(caminho, tamanho=(600, 600)):
    img = Image.open(caminho)  # abre a imagem
    img = img.convert('L')  # converte para tons de cinza
    img = img.resize(tamanho)  # redimensiona a imagem

    matriz = [[bin(img.getpixel((x, y)))[2:].zfill(8) for y in range(img.height)]
              for x in range(img.width)]  # cria a matriz
    
    for linha in matriz: # primeira e ultima coluna copiada
        linha.insert(0, linha[0])
        linha.append(linha[-1])
    
    matriz.insert(0, matriz[0]) # primeira linha copiada
    matriz.append(matriz[-1]) # ultima linha copiada

    # salva a matriz em um arquivo
    with open('matriz/matriz.txt', 'w') as arquivo:
        for index in range(len(matriz)):
            arquivo.write("\n".join(matriz[index]))
            if index != len(matriz) - 1:
                arquivo.write("\n")
