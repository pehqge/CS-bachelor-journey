[<kbd><img title="Português" alt="Português" src="https://flagicons.lipis.dev/flags/4x3/br.svg" width="22"></kbd> Versão em português](README.md)

# INE410159 - Computer Vision

**Group 7:** João Pedro Tamburo Faraoni, Leonardo de Sousa Marques, Pedro Henrique Gimenez and Tom Pereira Hunt.

Computer Vision and Pattern Recognition (INE5443) are the same course, taken together with a single deliverable, so everything lives here.

The project is **boxe.ml**: a command-line tool that takes the video of a boxing match and detects and classifies the punches thrown by each fighter. The code lives in the group's repository and comes in here as a submodule.

| Resource | What it is |
|---|---|
| [boxe.ml/](./boxe.ml) | Submodule with the project's code ([leonardosm14/boxe.ml](https://github.com/leonardosm14/boxe.ml), v1.0.0). |
| [boxe.ml/docs/paper/paper.pdf](./boxe.ml/docs/paper/paper.pdf) | Final report (in Portuguese). |
| [boxe.ml/docs/poster/poster.pdf](./boxe.ml/docs/poster/poster.pdf) | Project poster (in Portuguese). |
| [apresentacao.pdf](./apresentacao.pdf) | Final presentation slides (in Portuguese). |

## Detection and Classification of Boxing Punches

The pipeline has three stages. First **YOLOv8 Pose** extracts the fighters' skeletons frame by frame, with ByteTrack tracking to keep each fighter's identity across the video. Then an **LSTM** model trained in TensorFlow classifies the punch *type* from the trajectory of the keypoints: straight, hook or uppercut. Finally the punching *hand* (lead or rear) is decided by plain geometry over the keypoints, which expands the model's 3 classes into the 6 final ones: jab, cross, lead hook, lead uppercut, rear hook and rear uppercut.

The split exists because the punch type is learnable from the trajectory, but the hand is ambiguous within an isolated window: for each detected punch, the wrist with the largest net displacement is the one that threw it, and the direction of extension defines the local front, so the foot on that side is the *lead*.

Training used the [BoxingVI](https://github.com/Bikudebug/BoxingVI) benchmark, of which we got access to 5,463 annotated clips. The measured lead/rear accuracy was 0.74 on the test set and 0.89 per segment on the video we annotated ourselves.

Install and run instructions are in the [boxe.ml README](./boxe.ml/README.md).
