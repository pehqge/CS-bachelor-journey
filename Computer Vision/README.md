[<kbd><img title="English" alt="English" src="https://flagicons.lipis.dev/flags/4x3/us.svg" width="22"></kbd> English version](README_EN.md)

# INE410159 - Visão Computacional

**Grupo 7:** João Pedro Tamburo Faraoni, Leonardo de Sousa Marques, Pedro Henrique Gimenez e Tom Pereira Hunt

O trabalho é o **boxe.ml**, uma ferramenta de linha de comando que recebe o vídeo de uma luta de boxe e classifica os golpes de cada lutador. O YOLOv8 Pose extrai os esqueletos quadro a quadro com tracking ByteTrack, um LSTM em TensorFlow classifica o tipo do golpe pela trajetória dos keypoints (straight, hook ou uppercut) e a mão que golpeou sai de geometria sobre os mesmos keypoints, fechando as seis classes finais: jab, cross, lead hook, lead uppercut, rear hook e rear uppercut.

O código está no repositório do grupo e entra aqui como submódulo.

| Recurso | O que é |
|---|---|
| [boxe.ml/](./boxe.ml) | Código do projeto, submódulo de [leonardosm14/boxe.ml](https://github.com/leonardosm14/boxe.ml) na v1.0.0. Instalação e uso no [README interno](./boxe.ml/README.md). |
| [boxe.ml/docs/paper/paper.pdf](./boxe.ml/docs/paper/paper.pdf) | Relatório final, com os resultados medidos sobre o benchmark [BoxingVI](https://github.com/Bikudebug/BoxingVI). |
| [boxe.ml/docs/poster/poster.pdf](./boxe.ml/docs/poster/poster.pdf) | Pôster do trabalho. |
| [apresentacao.pdf](./apresentacao.pdf) | Slides da apresentação final. |
