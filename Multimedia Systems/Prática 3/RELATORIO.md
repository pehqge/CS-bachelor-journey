# Relatorio - Pratica III

**Disciplina:** INE5431 - Sistemas Multimidia
**Prof.:** Roberto Willrich

**Equipe:**
- Pedro Henrique Gimenez - 23102766
- Tom Pereira Hunt - 23102770

---

## Questao 1 - Analise do cabecalho BMP

Analisando `lena.bmp` no editor hexadecimal (primeiros bytes):

```
42 4D 36 00 0C 00 00 00 00 00 36 00 00 00 28 00
00 00 00 02 00 00 00 02 00 00 01 00 18 00 ...
```

- **Offset (bytes 10-13):** `36 00 00 00` = **54 bytes** (little-endian).
- **Tamanho do arquivo (bytes 2-5):** `36 00 0C 00` = **786486 bytes**.

A partir do offset 54 temos os dados da imagem. Lembrando que o BMP
armazena em ordem **BGR** e as linhas estao **invertidas** (o primeiro
pixel do arquivo corresponde a ultima linha da imagem).

Primeiros tres bytes em offset 54: `39 16 52`. Portanto o primeiro
pixel armazenado no arquivo tem:

- **B = 0x39 = 57**
- **G = 0x16 = 22**
- **R = 0x52 = 82**

---

## Questao 2 - Tamanho do cabecalho CUIF para o grupo

Pela especificacao do cabecalho CUIF:

| Campo              | Bytes              |
|--------------------|--------------------|
| Assinatura "CUIF"  | 4                  |
| Versao             | 1                  |
| Nestud             | 1                  |
| Largura            | 4                  |
| Altura             | 4                  |
| Matriculas         | 4 x Nestud         |

Nosso grupo tem **2 integrantes**, portanto:

`4 + 1 + 1 + 4 + 4 + (4 * 2) = ` **22 bytes**.

---

## Questao 3 - Implementacao do MSE e PSNR

Implementacao em `PraticaIII.py`:

```python
def MSE(ori, dec):
    largura = ori.width
    altura = ori.height
    n = largura * altura * 3  # 3 componentes por pixel

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
    mse = MSE(original, decodificada)
    if mse == 0:
        return float("inf")
    return 10 * math.log10(((2 ** b - 1) ** 2) / mse)
```

Seguindo as formulas da Secao 5 do enunciado:

- MSE(Ori, Dec) = (1/n) * sum((ori_i - dec_i)^2)
- PSNR(Ori, Dec) = 10 * log10( (2^b - 1)^2 / MSE )

---

## Questao 4 - PSNR CUIF.1

Comparando a imagem original (`lena.bmp`) com a decodificada a partir do
CUIF.1 (`lena1.bmp`):

```
PSNR (lena.bmp vs lena1.bmp) [CUIF.1]: inf (infinito)
```

**Justificativa:** o CUIF.1 nao aplica compressao com perdas. Ele apenas
reorganiza os pixels em sequencia por canal (primeiro todos os R, depois
todos os G, depois todos os B), mantendo os 8 bits originais de cada
componente. Portanto a imagem decodificada e identica, byte a byte, a
original: MSE = 0 e PSNR tende a infinito.

---

## Questao 5 - Compressao com zip

Tamanhos obtidos:

| Arquivo        | Tamanho (bytes) |
|----------------|-----------------|
| lena.bmp       | 786486          |
| lena1.cuif     | 786454          |
| lena.bmp.zip   | 733789          |
| lena1.cuif.zip | 643763          |

Taxas de compressao (tamanho do zip / tamanho do arquivo original):

- **lena.bmp.zip / lena.bmp** = 733789 / 786486 ≈ **0,9330 (93,30%)**
- **lena1.cuif.zip / lena1.cuif** = 643763 / 786454 ≈ **0,8185 (81,85%)**

**O CUIF.1 compactou mais.** Apesar de o `.cuif` e o `.bmp` sem
compressao terem praticamente o mesmo tamanho (a unica diferenca e o
cabecalho de 22 bytes do CUIF contra 54 do BMP), quando submetidos ao
zip o arquivo CUIF resulta em um zip significativamente menor.

**Explicacao:** o BMP intercala os canais pixel a pixel na ordem `B G R
B G R B G R ...`. Isso quebra a correlacao espacial entre os bytes
consecutivos: cada byte pertence a um canal diferente do vizinho,
entao a sequencia de bytes tem alta variacao local.

Ja o CUIF.1 organiza os dados canal-a-canal: primeiro todos os bytes do
canal R da imagem, depois todos do canal G, depois todos do canal B.
Bytes adjacentes passam a pertencer ao mesmo canal e geralmente a
pixels vizinhos da imagem, entao tem valores semelhantes. Essa
regularidade beneficia:

- **RLE (Run-Length Encoding):** mais sequencias de bytes iguais ou
  proximos → mais e maiores "runs".
- **DPCM (Differential PCM):** diferencas entre bytes consecutivos sao
  menores e concentradas em torno de zero, produzindo distribuicoes com
  baixa entropia.
- **Codificacao por dicionario (usada pelo DEFLATE/zip):** encontra
  mais padroes repetidos.

Verificando no editor hexadecimal, as regioes de dados do `lena1.cuif`
apresentam longos trechos de valores proximos (um canal por vez),
enquanto no `lena.bmp` os bytes oscilam fortemente a cada 3 bytes.

---

## Questao 6 - Geracao do CUIF.2 e principio da compressao

Alteramos o `PraticaIII.py` para gerar tambem o `lena2.cuif` usando
versao 2:

```python
cuif2 = Cuif(img, 2, matriculas)
cuif2.save("lena2.cuif")
cuif2_lido = Cuif.openCUIF("lena2.cuif")
cuif2_lido.saveBMP("lena2.bmp")
```

Comparando `lena1.bmp` e `lena2.bmp` visualmente, a `lena2.bmp`
apresenta leve perda de detalhe e pequenas bandas de cor nas regioes
mais suaves - efeito tipico da reducao de precisao dos canais G e B.

**Principio da compressao no CUIF.2** (analise do codigo em `Cuif.py`,
metodo `generateCUIF2`):

```python
gb = (b>>4) + (g&0xF0)
self.file_stream += struct.pack('%sB'%r.size, *r.flatten('F'))
self.file_stream += struct.pack('%sB'%gb.size, *gb.flatten('F'))
```

- O canal **R** e armazenado com seus 8 bits originais (1 byte por pixel).
- Os canais **G** e **B** sao quantizados para **4 bits cada**: mantem-se
  os 4 bits mais significativos e descartam-se os 4 menos significativos
  (`g & 0xF0` e `b >> 4`).
- Os 4 bits de G e os 4 bits de B sao empacotados num unico byte:
  `gb = (b >> 4) | (g & 0xF0)`, onde G ocupa os 4 bits altos e B os 4
  bits baixos do byte.

Portanto, cada pixel passa a ocupar 2 bytes (1 para R + 1 para GB
empacotado), contra 3 bytes no CUIF.1. E uma **compressao com perdas**
baseada em **quantizacao**: reduz-se a resolucao em profundidade dos
canais menos sensiveis a percepcao humana (G e B mantem menos detalhe
que R). Na decodificacao, os 4 bits baixos sao preenchidos com zeros
(ver `imgCUIF2` / `readCUIF2`), o que introduz o ruido de quantizacao.

---

## Questao 7 - Taxas de compressao CUIF.1 x CUIF.2

Tamanhos dos arquivos em relacao ao `lena.bmp` (786486 bytes):

| Arquivo      | Tamanho (bytes) | Razao cuif / bmp |
|--------------|-----------------|------------------|
| lena1.cuif   | 786454          | 0,99996 (~100%)  |
| lena2.cuif   | 524310          | 0,6666 (66,66%)  |

- **CUIF.1:** praticamente sem compressao (so economiza 32 bytes de
  cabecalho - 22 do CUIF contra 54 do BMP - e nao ha padding, mas neste
  caso a imagem 512x512 ja e multipla de 4, entao BMP tambem nao tem
  padding).
- **CUIF.2:** comprime para ~2/3 do tamanho do BMP. O calculo bate com
  o esperado: cada pixel ocupa 2 bytes em vez de 3, ou seja, 2/3 do
  tamanho original dos dados (`2 * 512 * 512 = 524288` bytes + 22 bytes
  de cabecalho = 524310 bytes, exatamente o tamanho observado).

**O CUIF.2 compactou mais**, as custas de perda de qualidade.

---

## Questao 8 - PSNR CUIF.2

Comparando `lena.bmp` com `lena2.bmp`:

```
PSNR (lena.bmp vs lena2.bmp) [CUIF.2]: 30,939 dB
```

**Justificativa:** o PSNR finito indica que houve perdas. A fonte do
ruido e a **quantizacao dos canais G e B** de 8 para 4 bits. Ao
descartar os 4 bits menos significativos de cada componente
(e ao recompor com zeros nesses 4 bits baixos na decodificacao), cada
amostra de G e B sofre um erro de ate 15 unidades (os valores possiveis
pos-quantizacao sao 0, 16, 32, ..., 240). O canal R nao contribui para
o erro pois mantem os 8 bits originais.

Um PSNR em torno de 31 dB e tipico de compressao com perdas moderada:
a imagem ainda e reconhecivel e utilizavel, mas apresenta artefatos
visiveis, especialmente banding em gradientes suaves dos canais G e B.
