# Relatorio - Pratica IV (Compressao de Entropia)

**Disciplina:** INE5431 - Sistemas Multimidia
**Prof.:** Roberto Willrich

**Equipe:**
- Pedro Henrique Gimenez - 23102766
- Tom Pereira Hunt - 23102770

---

## Resultados obtidos (sumario)

Tamanhos originais:
- `lena.bmp` = 786 486 bytes (512x512, 24 bpp)
- `teste.bmp` = 86 454 bytes (240x120, 24 bpp)

| Imagem   | Versao | Arquivo      | Tamanho (bytes) | Taxa (cuif / bmp) | PSNR (dB) |
|----------|--------|--------------|-----------------|-------------------|-----------|
| lena     | CUIF.1 | lena1.cuif   | 786 454         | 1,0000            | inf       |
| lena     | CUIF.2 | lena2.cuif   | 524 310         | 0,6666            | 30,939    |
| lena     | CUIF.3 | lena3.cuif   | 786 454         | 1,0000            | 38,597    |
| lena     | CUIF.4 | lena4.cuif   | 723 728         | 0,9202            | 33,222    |
| teste    | CUIF.1 | teste1.cuif  | 86 422          | 0,9996            | inf       |
| teste    | CUIF.2 | teste2.cuif  | 57 622          | 0,6665            | inf       |
| teste    | CUIF.3 | teste3.cuif  | 86 422          | 0,9996            | 47,225    |
| teste    | CUIF.4 | teste4.cuif  | 4 030           | 0,0466            | 35,228    |

---

## Questao 1 - Taxas de compressao

Definindo **taxa de compressao** como `tamanho(cuif) / tamanho(bmp)`
(quanto menor, mais compacto):

**Imagem lena.bmp:**
- CUIF.1: 786 454 / 786 486 = **1,0000** (praticamente igual ao BMP)
- CUIF.2: 524 310 / 786 486 = **0,6666** (~2/3 do BMP)
- CUIF.3: 786 454 / 786 486 = **1,0000** (igual ao CUIF.1)
- CUIF.4: 723 728 / 786 486 = **0,9202**

**Imagem teste.bmp:**
- CUIF.1: 86 422 / 86 454 = **0,9996**
- CUIF.2: 57 622 / 86 454 = **0,6665**
- CUIF.3: 86 422 / 86 454 = **0,9996**
- CUIF.4: 4 030 / 86 454 = **0,0466** (reducao a ~4,7% do tamanho original)

---

## Questao 2 - Qual codificacao comprimiu mais a imagem lena?

**CUIF.2 foi a mais eficiente para a lena** (taxa ≈ 0,6666, ~2/3 do BMP).

**Justificativa:**

- **CUIF.1** e **CUIF.3** apenas reorganizam os dados (canal-a-canal
  em RGB ou YCbCr) sem eliminar nenhum byte. Nao ha compressao: cada
  pixel continua ocupando 3 bytes. A unica diferenca em relacao ao BMP
  sao os 32 bytes economizados no cabecalho (22 do CUIF vs 54 do BMP),
  que sao desprezveis frente aos ~786 KB de dados.

- **CUIF.2** aplica **compressao com perdas por quantizacao**: reduz
  os canais G e B de 8 para 4 bits cada e empacota os dois em um unico
  byte. Assim cada pixel ocupa 2 bytes em vez de 3 (reducao para 2/3).
  E o mecanismo de compressao mais agressivo e determinstico dos quatro.

- **CUIF.4** aplica **codificacao de entropia (RLE)** sobre os dados
  em YCbCr. Para a lena, que e uma imagem fotografica com alta variacao
  entre pixels vizinhos, o RLE produz poucos "runs" longos e a compressao
  efetiva e pequena (taxa 0,92). Ou seja, a lena tem pouca redundancia
  espacial que o RLE consiga explorar.

Portanto, para a lena, o ganho vem mais da **reducao do numero de bits
por canal** (CUIF.2) do que da **supressao de repeticoes** (CUIF.4).

---

## Questao 3 - Por que o CUIF.4 comprime muito mais a teste do que a lena?

Taxas do CUIF.4: **lena = 0,9202** contra **teste = 0,0466**. A teste
ficou **~20 vezes mais compacta** em termos relativos.

A diferenca se deve ao principio do RLE: ele suprime **repeticoes
consecutivas** de um mesmo simbolo. Quanto maior a redundancia
sequencial nos dados, maior a compressao.

Analisando a teste.bmp com numpy:

- O canal **G tem apenas 1 valor unico (0)** em todos os 28 800 pixels.
- O canal **B tem apenas 1 valor unico (0)** em todos os 28 800 pixels.
- O canal **R tem apenas 32 valores distintos** (gradiente com 8 bits
  de passo entre eles: 0, 8, 16, 24, 33, 41, ...).
- Entre bytes consecutivos do canal R, **98,1%** sao iguais ao anterior.

Depois da conversao para YCbCr no CUIF.4:

- Cb e Cr ficam com valores praticamente constantes em grandes regioes
  (pois G e B sao 0 em toda a imagem).
- Y varia suavemente, acompanhando o gradiente de R.

O resultado sao longussimos "runs" de bytes identicos. O RLE codifica
cada run de N repeticoes com apenas 2 bytes (1 byte de flag+contagem,
1 byte do simbolo), entao a imagem comprime drasticamente: 4 030 bytes
a partir de 86 422 do CUIF.1 → taxa 4,66%.

Ja a lena.bmp e uma fotografia natural (a foto classica da modelo):
textura de cabelo, pele, chapeu, plano de fundo, todos com variacoes
suaves e ruido. Bytes consecutivos raramente sao iguais, runs longos
sao escassos e a compressao RLE mal consegue reduzir o arquivo (taxa
0,92).

**Resumo:** o RLE funciona bem em imagens com grandes areas uniformes
(sintecas, graficos, desenhos, como a teste) e mal em imagens naturais
com textura (como a lena).

---

## Questao 4 - PSNR das imagens lena1, lena2, lena3 e lena4

| Imagem decodificada | PSNR        | Fonte do ruido                                      |
|---------------------|-------------|-----------------------------------------------------|
| lena1.bmp (CUIF.1)  | **inf**     | Sem ruido - codificacao sem perdas                  |
| lena2.bmp (CUIF.2)  | **30,94 dB**| Quantizacao de G e B de 8 para 4 bits               |
| lena3.bmp (CUIF.3)  | **38,60 dB**| Arredondamento/truncamento na conversao RGB↔YCbCr   |
| lena4.bmp (CUIF.4)  | **33,22 dB**| Conversao YCbCr + deslocamento de 1 bit do RLE      |

### Justificativa de cada valor

**CUIF.1 - PSNR = inf.** A codificacao apenas reorganiza os pixels por
canal (primeiro todos os R, depois todos os G, depois todos os B)
sem alterar nenhum byte. A decodificacao reconstroi a imagem identica,
portanto MSE = 0 e PSNR = ∞.

**CUIF.2 - PSNR ≈ 30,94 dB.** O codificador descarta os 4 bits menos
significativos de G e B (`g & 0xF0`, `b & 0xF0`) e empacota os 4 bits
mais significativos em um byte. Na decodificacao, os 4 bits baixos
sao preenchidos com zeros, o que introduz erro de ate 15 unidades por
amostra nos canais G e B. O canal R nao contribui para o erro pois
mantem os 8 bits originais. E uma compressao com perdas determinstica
e esperada.

**CUIF.3 - PSNR ≈ 38,60 dB.** Apesar de o CUIF.3 ser conceitualmente
sem perdas (apenas reorganiza em YCbCr canal-a-canal), **a conversao
ida-e-volta entre RGB e YCbCr introduz ruido**. Os coeficientes da
transformada (0,299, 0,587, 0,114, 1,402, -0,34414, -0,71414, 1,772)
sao numeros reais e o codigo em `ColorSpace.py` usa `np.trunc(...)` e
`astype(np.uint8)`, descartando a parte fracionaria e saturando em 0
quando necessario. A cada pixel, entao, perde-se sub-unidade de
precisao nos tres canais, acumulando um ruido de quantizacao pequeno
mas sistematico. Esse erro e menor que o do CUIF.2 (PSNR maior ≈ 38,60
contra 30,94), pois a perda de precisao e de fracoes de unidade, e nao
dos 4 bits inteiros como no CUIF.2.

**CUIF.4 - PSNR ≈ 33,22 dB.** O CUIF.4 combina **duas fontes de erro**:
- O mesmo erro de conversao RGB↔YCbCr do CUIF.3 (~sub-unidade);
- O erro do RLE implementado em `RLE.py`: como a flag de repeticao
  ocupa o bit mais significativo, sobram apenas 7 bits para representar
  cada simbolo. A solucao adotada no codigo e dividir cada byte por 2
  (`np.right_shift(array, 1)`) antes da codificacao e multiplicar por
  2 (`data[i] << 1`) na decodificacao. Valores impares perdem
  irreversivelmente o bit menos significativo (sao zerados no retorno).
  Isso introduz um erro de ate 1 unidade em cada amostra de Y, Cb e Cr.

Observacao: o PSNR do CUIF.4 (33,22 dB) e **pior que o CUIF.3** (38,60),
como esperado, porque o CUIF.4 acumula o erro do CUIF.3 mais o ruido
do shift-1-bit; mas e **melhor que o CUIF.2** (30,94), porque 1 bit
perdido apenas em cada canal YCbCr e menos danoso que 4 bits perdidos
em G e B.

---

## Questao 5 - PSNR de teste2.bmp comparado com teste.bmp

**PSNR (teste.bmp vs teste2.bmp) = infinito.**

A primeira vista, isso contraria o esperado: o CUIF.2 e uma codificacao
com perdas, entao o PSNR deveria ser finito. Contudo, ao analisar o
conteudo da imagem `teste.bmp` com numpy:

```
canal R: 32 valores distintos (gradiente)
canal G: 1 unico valor (= 0)
canal B: 1 unico valor (= 0)
```

Ou seja, a imagem teste e um gradiente onde **G e B sao identicamente
zero** em todos os pixels. O CUIF.2 quantiza G e B descartando os 4
bits menos significativos, mas como esses canais valem 0 (e portanto
0x00 = 0000 0000 ja tem os 4 bits baixos zerados), nao ha informacao
a ser perdida. O canal R nao e alterado pelo CUIF.2.

Formalmente:
- Para todo pixel (i,j): `G(i,j) = 0` e `B(i,j) = 0`.
- Apos quantizacao: `G' = G & 0xF0 = 0`, `B' = B & 0xF0 = 0`.
- Logo `G' = G` e `B' = B` em toda a imagem.
- Como R tambem nao e alterado, a imagem decodificada e identica a
  original, MSE = 0 e PSNR = ∞.

Este caso ilustra que o CUIF.2 so introduz perda quando os 4 bits
menos significativos de G ou B contem informacao nao-nula. Em imagens
com paletas restritas e cores "redondas" (como a teste), a codificacao
pode ser efetivamente sem perdas - apesar de continuar comprimindo
para 2/3 do tamanho (taxa 0,6665).
