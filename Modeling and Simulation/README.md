[<kbd><img title="English" alt="English" src="https://flagicons.lipis.dev/flags/4x3/us.svg" width="22"></kbd> English version](README_EN.md)

# INE5425 - Modelagem e Simulação

**Autores:** Pedro Henrique Gimenez e João Vitor Curcio Sutter

O trabalho final da disciplina foi estender o GenESyS, o simulador de eventos discretos do professor Cancian, com um componente de autômatos celulares universais. Universal porque vizinhança, contorno, conjunto de estados e política de atualização são configuráveis, o que cobre desde as regras elementares de Wolfram até o Jogo da Vida; e porque o usuário pode escrever a própria regra local em C++ pela interface do simulador, compilada e carregada em tempo de execução. São 50 testes em gtest, verificados no Linux.

A entrega foi um pull request no repositório oficial do GenESyS, já mergeado. A branch em que trabalhamos entra aqui como submódulo, fixada no commit da entrega.

| Recurso | O que é |
|---|---|
| [Genesys-Simulator-cellular-automata/](./Genesys-Simulator-cellular-automata) | O código, na branch `tema6-2026-1` do fork. |
| [#453](https://github.com/rlcancian/Genesys-Simulator/issues/453) | O pull request para `rlcancian:2026-1`, mergeado em 10/07/2026. |
| [apresentacao.pdf](./apresentacao.pdf) | Slides da apresentação final. |
