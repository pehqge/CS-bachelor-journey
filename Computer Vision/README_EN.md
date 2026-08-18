[<kbd><img title="Português" alt="Português" src="https://flagicons.lipis.dev/flags/4x3/br.svg" width="22"></kbd> Versão em português](README.md)

# INE410159 - Computer Vision

**Group 7:** João Pedro Tamburo Faraoni, Leonardo de Sousa Marques, Pedro Henrique Gimenez and Tom Pereira Hunt

The project is **boxe.ml**, a command-line tool that takes the video of a boxing match and classifies each fighter's punches. YOLOv8 Pose extracts the skeletons frame by frame with ByteTrack tracking, an LSTM in TensorFlow classifies the punch type from the keypoint trajectory (straight, hook or uppercut), and the punching hand comes out of geometry over those same keypoints, closing the six final classes: jab, cross, lead hook, lead uppercut, rear hook and rear uppercut.

The code lives in the group's repository and comes in here as a submodule.

| Resource | What it is |
|---|---|
| [boxe.ml/](./boxe.ml) | Project code, submodule of [leonardosm14/boxe.ml](https://github.com/leonardosm14/boxe.ml) at v1.0.0. Install and usage in the [inner README](./boxe.ml/README.md). |
| [boxe.ml/docs/paper/paper.pdf](./boxe.ml/docs/paper/paper.pdf) | Final report, with the results measured on the [BoxingVI](https://github.com/Bikudebug/BoxingVI) benchmark. In Portuguese. |
| [boxe.ml/docs/poster/poster.pdf](./boxe.ml/docs/poster/poster.pdf) | Project poster. In Portuguese. |
| [apresentacao.pdf](./apresentacao.pdf) | Final presentation slides. In Portuguese. |
