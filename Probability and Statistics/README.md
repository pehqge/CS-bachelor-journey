[<kbd><img title="English" alt="English" src="https://flagicons.lipis.dev/flags/4x3/us.svg" width="22"></kbd> English version](README_EN.md)

# INE5405 - Probabilidade e Estatística

**Grupo:** Pedro Henrique Gimenez, [Beatriz Repette](https://github.com/beatriz-repette), [Diego Meditsch](https://github.com/DMeditsch) e [Tom Hunt](https://github.com/tmphnt)

Os dois trabalhos analisam o acervo público do Metropolitan Museum of Art (MET), restrito a pinturas e esculturas: partimos de cerca de 480 mil peças e ficamos com 15.124 obras. O [Trabalho 1](Trabalho%201) é a análise exploratória e o [Trabalho 2](Trabalho%202) é a inferência estatística sobre os mesmos dados. Cada um tem o relatório em `documento`, o código em `codigos`, os dados em `data` e os gráficos em `imagens`.

## Trabalho 1: análise exploratória

Descrição das obras por material, cultura, época e popularidade (a variável Is Highlight do museu), com estatística descritiva e gráficos cruzando essas variáveis.

| Arquivo | O que é |
|---------|---------|
| [documento/trabalho1.pdf](Trabalho%201/documento/trabalho1.pdf) | Relatório final, com a fonte LaTeX ao lado. |
| [codigos/variaveis](Trabalho%201/codigos/variaveis) | Scripts Python que resumem cada variável. |
| [codigos/combinacao](Trabalho%201/codigos/combinacao) | Scripts R dos gráficos que cruzam variáveis: pareto, violino, pizza e densidade. |
| [imagens](Trabalho%201/imagens) | Gráficos gerados. |
| [tabela_met.csv](Trabalho%201/tabela_met.csv) | Base bruta exportada do MET. |

## Trabalho 2: inferência estatística

Quatro hipóteses testadas: a média da área das pinturas destaque contra as não destaque, a proporção de tema religioso entre os destaques, a correlação entre ano e popularidade, e a regressão do volume da escultura pelo ano de confecção.

| Arquivo | O que é |
|---------|---------|
| [documento/trabalho2.pdf](Trabalho%202/documento/trabalho2.pdf) | Relatório final, com a fonte LaTeX ao lado. |
| [codigos](Trabalho%202/codigos) | Scripts Python e R dos testes de hipótese e do tratamento dos dados. |
| [data](Trabalho%202/data) | CSVs tratados do MET, com README explicando os dois formatos. |
| [imagens/regressao_linear.png](Trabalho%202/imagens/regressao_linear.png) | Gráfico da regressão linear. |

O [Aulas/regressao.py](Aulas/regressao.py) é um exercício de correlação de Pearson e regressão feito em aula, fora dos trabalhos.
