# INE5431 - Sistemas Multimidia
# Pratica III - Representacao digital de imagens (CUIF)
# Membros da equipe:
#  Pedro Henrique Gimenez  - 23102766
#  Tom Pereira Hunt        - 23102770

from PIL import Image
from Cuif import Cuif
import math
import os


def MSE(ori, dec):
    """Media dos Erros Quadraticos entre duas imagens RGB.

    n = largura * altura * 3 (3 componentes por pixel)
    MSE = (1/n) * soma( (ori_i - dec_i)^2 )
    """
    largura = ori.width
    altura = ori.height
    n = largura * altura * 3

    soma = 0
    for i in range(largura):
        for j in range(altura):
            ori_r, ori_g, ori_b = ori.getpixel((i, j))
            dec_r, dec_g, dec_b = dec.getpixel((i, j))
            soma += (ori_r - dec_r) ** 2
            soma += (ori_g - dec_g) ** 2
            soma += (ori_b - dec_b) ** 2

    return soma / n


def PSNR(original, decodificada, b):
    """PSNR em dB. Retorna 'Infinito' quando MSE = 0 (imagens identicas)."""
    try:
        mse = MSE(original, decodificada)
        if mse == 0:
            return float("inf")
        psnr = 10 * math.log10(((2 ** b - 1) ** 2) / mse)
        return psnr
    except ZeroDivisionError:
        return float("inf")


def taxa_compressao(arq_compactado, arq_original):
    """Razao tamanho(compactado) / tamanho(original)."""
    t_comp = os.path.getsize(arq_compactado)
    t_orig = os.path.getsize(arq_original)
    return t_comp / t_orig, t_comp, t_orig


if __name__ == "__main__":
    filepath = "lena.bmp"
    img = Image.open(filepath)
    matriculas = [20205642, 2022423]

    # --- CUIF.1 ------------------------------------------------------------
    # Instancia objeto Cuif convertendo imagem em CUIF.1
    cuif1 = Cuif(img, 1, matriculas)

    # Imprime cabecalho Cuif (mostra tambem as matriculas do grupo)
    print("=== Cabecalho CUIF.1 ===")
    cuif1.printHeader()

    # Gera o arquivo .cuif
    cuif1.save("lena1.cuif")

    # Conversao inversa: abre o arquivo .cuif e salva como BMP
    cuif1_lido = Cuif.openCUIF("lena1.cuif")
    cuif1_lido.saveBMP("lena1.bmp")

    # Carrega decodificada para calcular PSNR
    img_lena1 = Image.open("lena1.bmp")
    psnr1 = PSNR(img, img_lena1, 8)
    print(f"\nPSNR (lena.bmp vs lena1.bmp) [CUIF.1]: {psnr1}")

    # --- CUIF.2 ------------------------------------------------------------
    cuif2 = Cuif(img, 2, matriculas)

    print("\n=== Cabecalho CUIF.2 ===")
    cuif2.printHeader()

    cuif2.save("lena2.cuif")

    cuif2_lido = Cuif.openCUIF("lena2.cuif")
    cuif2_lido.saveBMP("lena2.bmp")

    img_lena2 = Image.open("lena2.bmp")
    psnr2 = PSNR(img, img_lena2, 8)
    print(f"\nPSNR (lena.bmp vs lena2.bmp) [CUIF.2]: {psnr2}")

    # --- Taxas de compressao dos formatos CUIF em relacao ao BMP ----------
    print("\n=== Taxas de compressao (cuif / bmp) ===")
    razao1, t1, tbmp = taxa_compressao("lena1.cuif", "lena.bmp")
    razao2, t2, _ = taxa_compressao("lena2.cuif", "lena.bmp")
    print(f"lena.bmp   : {tbmp} bytes")
    print(f"lena1.cuif : {t1} bytes  ->  razao = {razao1:.4f}  ({razao1*100:.2f}%)")
    print(f"lena2.cuif : {t2} bytes  ->  razao = {razao2:.4f}  ({razao2*100:.2f}%)")

    # Visualiza as imagens para comparacao visual
    # img.show()
    # img_lena1.show()
    # img_lena2.show()
