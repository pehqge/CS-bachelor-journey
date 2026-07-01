[<kbd><img title="English" alt="English" src="https://flagicons.lipis.dev/flags/4x3/us.svg" width="22"></kbd> English version](README_EN.md)

# INE5405 - Probabilidade e Estatística

**Grupo:** Pedro Henrique Gimenez, [Beatriz Repette](https://github.com/beatriz-repette), [Diego Meditsch](https://github.com/DMeditsch) e [Tom Hunt](https://github.com/tmphnt)

Estudei análise combinatória, probabilidade, variáveis aleatórias discretas e contínuas, estimação de parâmetros e testes de hipóteses.

Os dois trabalhos são análises sobre o acervo público do Metropolitan Museum of Art (MET), restritas a pinturas e esculturas. Partimos de cerca de 480 mil peças e ficamos com 15.124 obras. Cada trabalho tem o relatório (`documento`), o código (`codigos`), os dados (`data`) e os gráficos (`imagens`).

| Pasta | O que é |
|-------|---------|
| [Aulas/regressao.py](Aulas/regressao.py) | Exercício de correlação de Pearson e regressão feito em aula. |
| [Trabalho 1](Trabalho%201) | Análise exploratória do acervo do MET. |
| [Trabalho 2](Trabalho%202) | Inferência estatística sobre os mesmos dados. |

## Trabalho 1: análise exploratória

Descrevemos as obras por material, cultura, época e popularidade (a variável Is Highlight do museu), usando estatística descritiva e gráficos cruzando essas variáveis.

| Arquivo | O que é |
|---------|---------|
| [documento/trabalho1.pdf](Trabalho%201/documento/trabalho1.pdf) | Relatório final. |
| [documento/trabalho1.tex](Trabalho%201/documento/trabalho1.tex) | Fonte LaTeX do relatório. |
| [codigos/variaveis](Trabalho%201/codigos/variaveis) | Scripts Python que resumem cada variável. |
| [codigos/combinacao](Trabalho%201/codigos/combinacao) | Scripts R dos gráficos que cruzam variáveis (pareto, violino, pizza, densidade). |
| [imagens](Trabalho%201/imagens) | Gráficos gerados. |
| [tabela_met.csv](Trabalho%201/tabela_met.csv) | Base bruta exportada do MET. |
| [tarefas.md](Trabalho%201/tarefas.md) | Lista de variáveis e gráficos planejados. |

## Trabalho 2: inferência estatística

Testamos quatro hipóteses sobre os dados: a média da área das pinturas destaque contra as não destaque, a proporção de tema religioso entre os destaques, a correlação entre ano e popularidade, e a regressão do volume da escultura pelo ano de confecção.

| Arquivo | O que é |
|---------|---------|
| [documento/trabalho2.pdf](Trabalho%202/documento/trabalho2.pdf) | Relatório final. |
| [documento/trabalho2.tex](Trabalho%202/documento/trabalho2.tex) | Fonte LaTeX do relatório. |
| [codigos](Trabalho%202/codigos) | Scripts Python e R dos testes de hipótese e do tratamento dos dados. |
| [data](Trabalho%202/data) | CSVs tratados do MET, com README explicando os dois formatos. |
| [imagens/regressao_linear.png](Trabalho%202/imagens/regressao_linear.png) | Gráfico da regressão linear. |
