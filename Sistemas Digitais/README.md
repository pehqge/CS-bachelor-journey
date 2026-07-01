[<kbd><img title="English" alt="English" src="https://flagicons.lipis.dev/flags/4x3/us.svg" width="22"></kbd> English version](README_EN.md)

# INE5406 - Sistemas Digitais

Esta disciplina continua o que vi em Circuitos Digitais, agora com projeto de hardware em VHDL na placa FPGA. Os trabalhos em grupo eu fiz com a Victória Rodrigues. A parte prática tem as atividades feitas em aula (na pasta [Aulas](./Aulas)) e quatro práticas avaliativas ao longo do semestre. As três primeiras giram em torno da SAD (soma de diferenças absolutas), em duas versões (v1 e v3), e a última é um módulo de convolução com filtro gaussiano.

## Práticas avaliativas

| Prática | Descrição |
| --- | --- |
| [Prática 1](./Prática%201) | Mux 4x1, demux 1x4 e decodificador BCD para 7 segmentos em duas formas (expressões lógicas e case). Tem relatório com as simulações. |
| [Prática 2](./Prática%202) | SAD v1 e v3 montadas com componentes genéricos (subtrator, somador, somador com overflow, mux e registrador). Relatório com as simulações e a análise de atraso. |
| [Prática 3](./Prática%203) | SAD v1 e v3 com testbench e golden model, usando estímulos aleatórios gerados em Python. |
| [Prática 4](./Prática%204) | Módulo de convolução (filtro gaussiano) em VHDL, com scripts Python para gerar e filtrar as matrizes de teste. Inclui o relatório em PDF e o RTL. |

## Atividades em aula

| Atividade | Descrição |
| --- | --- |
| [Aula 4](./Aulas/Aula%204) | Registrador de 4 bits e flip-flop tipo D, com o arquivo de estímulos para simular. |
