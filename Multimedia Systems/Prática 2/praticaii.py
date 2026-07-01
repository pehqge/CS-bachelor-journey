# Sistemas Multimidia
# Pratica II - Manipulacao de Imagens com Python


# Membros da equipe:
#  Pedro Henrique Gimenez
#  Tom Pereira Hunt

from PIL import Image


def reduzir_resolucao(img):
    """Reduz a resolucao da imagem para 1/4 da altura e da largura."""
    
    largura = img.size[0]
    altura = img.size[1]
    raster_orig = img.load()

    nova_largura = largura // 4
    nova_altura = altura // 4

    img_nova = Image.new("RGB", (nova_largura, nova_altura))
    raster_nova = img_nova.load()

    for i in range(nova_largura):
        for j in range(nova_altura):
            # pega o pixel correspondente da imagem original
            r, g, b = raster_orig[i * 4, j * 4]
            raster_nova[i, j] = (r, g, b) 

    return img_nova


def converter_tons_de_cinza(img):
    """Converte a imagem RGB para tons de cinza usando Y = 0.3R + 0.59G + 0.11B."""
    largura = img.size[0]
    altura = img.size[1]
    raster_orig = img.load()

    img_cinza = Image.new("L", (largura, altura))
    raster_cinza = img_cinza.load()

    for i in range(largura):
        for j in range(altura):
            r, g, b = raster_orig[i, j]
            y = int(0.3 * r + 0.59 * g + 0.11 * b)
            raster_cinza[i, j] = y

    return img_cinza


def converter_binaria(img):
    """Converte a imagem RGB para binaria (preto e branco)."""
    largura = img.size[0]
    altura = img.size[1]
    raster_orig = img.load()

    img_bin = Image.new("1", (largura, altura))
    raster_bin = img_bin.load()

    for i in range(largura):
        for j in range(altura):
            r, g, b = raster_orig[i, j]
            y = int(0.3 * r + 0.59 * g + 0.11 * b)
            if y >= 127:
                raster_bin[i, j] = 1  # branco
            else:
                raster_bin[i, j] = 0  # preto

    return img_bin


def reduzir_bits(img):
    """Simula reducao para 4 bits por canal, mantendo apenas os 4 bits mais significativos."""
    largura = img.size[0]
    altura = img.size[1]
    raster_orig = img.load()

    img_4bits = Image.new("RGB", (largura, altura))
    raster_4bits = img_4bits.load()

    # mascara 0xF0 = 1111 0000 em binario, zera os 4 bits menos significativos
    mascara = 0xF0

    for i in range(largura):
        for j in range(altura):
            r, g, b = raster_orig[i, j]
            r_novo = r & mascara
            g_novo = g & mascara
            b_novo = b & mascara
            raster_4bits[i, j] = (r_novo, g_novo, b_novo)

    return img_4bits


def separar_canais_rgb(img):
    """Separa os canais R, G e B da imagem original, retornando 3 imagens coloridas."""
    largura = img.size[0]
    altura = img.size[1]
    raster_orig = img.load()

    img_r = Image.new("RGB", (largura, altura))
    img_g = Image.new("RGB", (largura, altura))
    img_b = Image.new("RGB", (largura, altura))

    raster_r = img_r.load()
    raster_g = img_g.load()
    raster_b = img_b.load()

    for i in range(largura):
        for j in range(altura):
            r, g, b = raster_orig[i, j]
            # canal R: so vermelho, zero nos outros
            raster_r[i, j] = (r, 0, 0)
            # canal G: so verde, zero nos outros
            raster_g[i, j] = (0, g, 0)
            # canal B: so azul, zero nos outros
            raster_b[i, j] = (0, 0, b)

    return img_r, img_g, img_b

# Carrega a imagem peixe.png do arquivo local
img = Image.open("peixe.png")
print("Imagem original - Largura:", img.size[0], "Altura:", img.size[1])
img.show()

# 1. Reducao de resolucao (1/4 largura e 1/4 altura)
img_reduzida = reduzir_resolucao(img)
print("Imagem reduzida - Largura:", img_reduzida.size[0], "Altura:", img_reduzida.size[1])
img_reduzida.show()

# 2. Conversao para tons de cinza
img_cinza = converter_tons_de_cinza(img)
print("Imagem em tons de cinza gerada")
img_cinza.show()

# 3. Conversao para imagem binaria
img_binaria = converter_binaria(img)
print("Imagem binaria gerada")
img_binaria.show()

# 4. Reducao para 4 bits por canal
img_4bits = reduzir_bits(img)
print("Imagem com 4 bits por canal gerada")
img_4bits.show()

# 5. Separacao dos canais RGB
img_r, img_g, img_b = separar_canais_rgb(img)
print("Canais R, G e B separados")
img_r.show()
img_g.show()
img_b.show()
