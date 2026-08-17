[<kbd><img title="English" alt="English" src="https://flagicons.lipis.dev/flags/4x3/us.svg" width="22"></kbd> English version](README_EN.md)

# INE5425 - Modelagem e Simulação

**Autores:** Pedro Henrique Gimenez e João Vitor Curcio Sutter
**Semestre:** 7º · 2026.1

O trabalho final da disciplina (DCS, Desenvolvimento de Componente de Simulação) foi estender o **GenESyS**, o simulador de eventos discretos do professor Cancian, com um componente de **autômatos celulares universais com regra local definida pelo usuário** (tema 6.2).

A entrega é um pull request no repositório oficial do GenESyS, que já foi mergeado. A branch em que trabalhamos entra aqui como submódulo, então o que está fixado abaixo é exatamente o código entregue.

| Recurso | O que é |
|---|---|
| [Genesys-Simulator-cellular-automata/](./Genesys-Simulator-cellular-automata) | Submódulo fixado na branch `tema6-2026-1` do fork, a branch da nossa entrega. |
| [#453](https://github.com/rlcancian/Genesys-Simulator/issues/453) | O pull request para `rlcancian:2026-1`, mergeado em 10/07/2026. |
| [apresentacao.pdf](./apresentacao.pdf) | Slides da apresentação final. |

## O componente

O componente modela um autômato celular como um elemento de simulação do GenESyS: um reticulado de células com estado, uma vizinhança e uma regra local que decide o próximo estado de cada célula a partir dos vizinhos.

A parte "universal" é poder configurar cada uma dessas peças em vez de fixá-las: vizinhança de Moore ou von Neumann, contornos fixo, espelhado, periódico ou adiabático, conjuntos de estado de bit, inteiro ou real, e políticas de atualização síncrona, sequencial, aleatória ou em blocos. Com isso o mesmo componente reproduz desde as regras elementares de Wolfram (30, 90, 110) até o Jogo da Vida.

A **regra local definida pelo usuário** é a minha parte: em vez de escolher uma regra pronta, o usuário escreve o corpo da função em C++ pela interface do simulador e o componente compila esse código em tempo de execução (via o `CppCompiler` que já existia no GenESyS), carrega a biblioteca resultante e chama a função a cada passo. O contrato é `nextState(self, neighbors, numNeighbors)`, com uma variante estendida que também recebe a posição da célula, para regras que dependem de onde ela está. O código do usuário passa por validação de tamanho e por uma blocklist antes de ir para o compilador, e a persistência do modelo salva e recarrega a regra junto com o resto da configuração.

O componente tem **50 testes** em gtest, verificados no Linux, cobrindo as regras elementares contra os resultados do livro, o Jogo da Vida, os quatro tipos de contorno, as políticas de atualização, a regra do usuário e a persistência.
