from PIL import Image

def line_to_matrix(arquivo):
    with open(arquivo, 'r') as file: # abre o arquivo e salva o conteudo em uma string
        string = file.read()

    # descobre o tamanho da matriz
    num_linhas = string.count('\n')+1
    tam_matriz = int(num_linhas**0.5)

    matriz_a = string.split('\n') # separa a string em uma lista

    # cria a matriz
    matriz = []
    for i in range(tam_matriz):
        matriz.append(matriz_a[:tam_matriz])
        matriz_a = matriz_a[tam_matriz:]
        
    return matriz

def matrix_to_img(caminho_matriz, caminho_salvar):
    # recebe o arquivo com a matriz
    matriz = line_to_matrix(caminho_matriz)

    # cria uma nova imagem preto e branco (L) com o tamanho da matriz
    img = Image.new('L', (len(matriz), len(matriz[0])))

    for x in range(img.width):  # percorre a imagem e a cria
        for y in range(img.height):
            img.putpixel((x, y), int(matriz[x][y], 2))

    img.save(caminho_salvar)  # salva a imagem
