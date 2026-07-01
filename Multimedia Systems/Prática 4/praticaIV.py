"""
INE5431 - Sistemas Multimidia
Pratica IV: Compressao de Entropia

Membros da equipe:
  Pedro Henrique Gimenez - 23102766
  Tom Pereira Hunt       - 23102770
"""

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
            return "Infinito"
        return 10 * math.log10(((2 ** b - 1) ** 2) / mse)
    except ZeroDivisionError:
        return "Infinito"


def processar(imagem_bmp, prefixo, versoes, matriculas):
    """Codifica/decodifica a imagem nas versoes CUIF indicadas, gerando arquivos
    <prefixo><v>.cuif e <prefixo><v>.bmp, e imprimindo taxa de compressao e PSNR.
    """
    img = Image.open(imagem_bmp)
    tam_bmp = os.path.getsize(imagem_bmp)

    print(f"\n=== {imagem_bmp}  ({img.size[0]}x{img.size[1]}, {tam_bmp} bytes) ===")

    for v in versoes:
        nome_cuif = f"{prefixo}{v}.cuif"
        nome_bmp = f"{prefixo}{v}.bmp"

        # Codifica a imagem no formato CUIF.v e salva o arquivo
        cuif = Cuif(img, v, matriculas)
        cuif.save(nome_cuif)

        # Le de volta o arquivo CUIF e salva a imagem decodificada como BMP
        cuif_lido = Cuif.openCUIF(nome_cuif)
        cuif_lido.saveBMP(nome_bmp)

        # Metricas
        tam_cuif = os.path.getsize(nome_cuif)
        taxa = tam_cuif / tam_bmp
        img_dec = Image.open(nome_bmp)
        psnr = PSNR(img, img_dec, 8)

        print(
            f"  CUIF.{v}: {nome_cuif:<14} {tam_cuif:>8} bytes  "
            f"taxa = {taxa:.4f} ({taxa*100:.2f}%)  "
            f"PSNR = {psnr}"
        )


if __name__ == "__main__":
    # Matriculas do grupo
    matriculas = [23102766, 23102770]

    # Processa as duas imagens nas 4 versoes do padrao CUIF
    processar("lena.bmp", "lena", [1, 2, 3, 4], matriculas)
    processar("teste.bmp", "teste", [1, 2, 3, 4], matriculas)
