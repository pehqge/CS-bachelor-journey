[<kbd><img title="Português" alt="Português" src="https://flagicons.lipis.dev/flags/4x3/br.svg" width="22"></kbd> Versão em português](README.md)

# EEL5105 - Digital Circuits and Techniques

This is the work I did in this course. Classes were both theory and lab, and in the labs I programmed in VHDL on the DE1-SoC FPGA board. The practical part has the in-class activities (in the [Aulas](./Aulas) folder), four graded exercises over the semester and a final project. The files are VHDL, with testbenches when the task asked for simulation.

## In-class activities

The in-class activities are grouped in the [Aulas](./Aulas) folder.

| Activity | Description |
| --- | --- |
| [Aula 1](./Aulas/Aula%201) | Half adder, full adder and a few variations (majority, xtreme_adder). |
| [Aula 2](./Aulas/Aula%202) | Two's complement to hexadecimal, using a mux and a binary to decimal converter. |
| [Aula 3](./Aulas/Aula%203) | An adder wired to a 7-segment display and a circuit that multiplies by 3. |
| [Aula 4](./Aulas/Aula%204) | VHDL testbenches for the full adder, mult3 and a 4-bit adder. |
| [Aula 5](./Aulas/Aula%205) | D flip-flop and clock-driven registers. |
| [Aula 6](./Aulas/Aula%206) | A finite state machine with its testbench for simulation. |

## Graded exercises

| Exercise | Description |
| --- | --- |
| [Exercício 1](./Exercício%201) | Combinational circuit with four inputs and four outputs, built from Karnaugh maps. |
| [Exercício 2](./Exercício%202) | Binary to BCD and BCD to 7-segment converters, an 8-bit adder, a divide-by-4 and a mux. |
| [Exercício 3](./Exercício%203) | A counter shown on two 7-segment displays, with a minimum signal. |
| [Exercício 4](./Exercício%204) | Finite state machine with testbench. |

## Final project

| Project | Description |
| --- | --- |
| [Trabalho Final](./Trabalho%20Final) | FPGA memory game, with datapath, control block, ROMs and decoders. |

The final project is a memory game on the FPGA. The player picks a difficulty and starts. For a few seconds numbers from 1 to 15 in hexadecimal show up and must be memorized. Then the player has 10 seconds to set them on the board switches.

### How it works
![Screenshot 26-06-2023 at 03 07](https://github.com/pehqge/UFSC/assets/117869493/985aa414-4cb4-4123-bfae-81c4c0c25666)

### Circuit
<img width="721" alt="Screenshot 26-06-2023 at 04 18" src="https://github.com/pehqge/UFSC/assets/117869493/e2148cf6-6835-49fd-9af3-92c31f4976de">
