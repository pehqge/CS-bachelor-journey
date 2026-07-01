[<kbd><img title="English" alt="English" src="https://flagicons.lipis.dev/flags/4x3/us.svg" width="22"></kbd> English version](README_EN.md)

# EEL5105 - Circuitos e Técnicas Digitais

Aqui estão os trabalhos que fiz nessa disciplina. As aulas eram teóricas e práticas, e nos laboratórios eu programei em VHDL na placa FPGA DE1-SoC. A parte prática tem as atividades feitas em aula (na pasta [Aulas](./Aulas)), quatro exercícios avaliativos ao longo do semestre e um trabalho final. Os arquivos são em VHDL, com testbenches quando o trabalho pedia simulação.

## Atividades em aula

As atividades feitas em aula estão agrupadas na pasta [Aulas](./Aulas).

| Atividade | Descrição |
| --- | --- |
| [Aula 1](./Aulas/Aula%201) | Meio somador, somador completo e algumas variações (majority, xtreme_adder). |
| [Aula 2](./Aulas/Aula%202) | Conversão de complemento de dois para hexadecimal, usando mux e um conversor binário para decimal. |
| [Aula 3](./Aulas/Aula%203) | Somador ligado a display de 7 segmentos e um circuito que multiplica por 3. |
| [Aula 4](./Aulas/Aula%204) | Testbenches em VHDL para o full adder, o mult3 e um somador de 4 bits. |
| [Aula 5](./Aulas/Aula%205) | Flip-flop tipo D e registradores sincronizados por clock. |
| [Aula 6](./Aulas/Aula%206) | Uma máquina de estados finitos com o testbench para simular. |

## Exercícios avaliativos

| Exercício | Descrição |
| --- | --- |
| [Exercício 1](./Exercício%201) | Circuito combinacional com quatro entradas e quatro saídas, montado a partir de mapas de Karnaugh. |
| [Exercício 2](./Exercício%202) | Conversores binário para BCD e BCD para 7 segmentos, somador de 8 bits, divisor por 4 e mux. |
| [Exercício 3](./Exercício%203) | Contador exibido em dois displays de 7 segmentos, com sinal de mínimo. |
| [Exercício 4](./Exercício%204) | Máquina de estados finitos com testbench. |

## Trabalho final

| Trabalho | Descrição |
| --- | --- |
| [Trabalho Final](./Trabalho%20Final) | Jogo da memória para FPGA, com datapath, bloco de controle, ROMs e decodificadores. |

O trabalho final é um jogo da memória na FPGA. O jogador escolhe um nível de dificuldade e começa. Por alguns segundos aparecem números de 1 a 15 em hexadecimal, e ele precisa memorizá-los. Depois tem 10 segundos para marcá-los nos switches da placa.

### Funcionamento
![Screenshot 26-06-2023 at 03 07](https://github.com/pehqge/UFSC/assets/117869493/985aa414-4cb4-4123-bfae-81c4c0c25666)

### Circuito
<img width="721" alt="Screenshot 26-06-2023 at 04 18" src="https://github.com/pehqge/UFSC/assets/117869493/e2148cf6-6835-49fd-9af3-92c31f4976de">
