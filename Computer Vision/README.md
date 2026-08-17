[<kbd><img title="English" alt="English" src="https://flagicons.lipis.dev/flags/4x3/us.svg" width="22"></kbd> English version](README_EN.md)

# INE410159 - Visão Computacional

**Grupo 7:** João Pedro Tamburo Faraoni, Leonardo de Sousa Marques, Pedro Henrique Gimenez e Tom Pereira Hunt.

Visão Computacional e Reconhecimento de Padrões (INE5443) são a mesma disciplina, cursadas juntas e com uma entrega só, então tudo fica aqui.

O trabalho é o **boxe.ml**: uma ferramenta de linha de comando que recebe o vídeo de uma luta de boxe e detecta e classifica os golpes de cada lutador. O código fica no repositório do grupo e entra aqui como submódulo.

| Recurso | O que é |
|---|---|
| [boxe.ml/](./boxe.ml) | Submódulo com o código do projeto ([leonardosm14/boxe.ml](https://github.com/leonardosm14/boxe.ml), v1.0.0). |
| [boxe.ml/docs/paper/paper.pdf](./boxe.ml/docs/paper/paper.pdf) | Relatório final. |
| [boxe.ml/docs/poster/poster.pdf](./boxe.ml/docs/poster/poster.pdf) | Pôster do trabalho. |
| [apresentacao.pdf](./apresentacao.pdf) | Slides da apresentação final. |

## Detecção e Classificação de Golpes em Boxe

O pipeline tem três etapas. Primeiro o **YOLOv8 Pose** extrai os esqueletos dos lutadores quadro a quadro, com tracking ByteTrack para manter a identidade de cada um ao longo do vídeo. Depois um modelo **LSTM** treinado em TensorFlow classifica o *tipo* do golpe pela trajetória dos keypoints: straight, hook ou uppercut. Por fim, a *mão* do golpe (lead ou rear) é decidida por geometria pura sobre os keypoints, o que expande as 3 classes do modelo para as 6 classes finais: jab, cross, lead hook, lead uppercut, rear hook e rear uppercut.

A separação existe porque o tipo do golpe é aprendível da trajetória, mas a mão é ambígua numa janela isolada: em cada golpe detectado, o punho de maior deslocamento líquido define a mão que golpeou, e a direção de extensão define a frente local, então o pé desse lado é o *lead*.

O treino usou o benchmark [BoxingVI](https://github.com/Bikudebug/BoxingVI), do qual tivemos acesso a 5.463 clipes anotados. A acurácia lead/rear medida foi de 0,74 no conjunto de teste e 0,89 por segmento no vídeo próprio que anotamos.

As instruções de instalação e execução estão no [README do boxe.ml](./boxe.ml/README.md).
