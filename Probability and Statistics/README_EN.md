[<kbd><img title="Português" alt="Português" src="https://flagicons.lipis.dev/flags/4x3/br.svg" width="22"></kbd> Versão em português](README.md)

# INE5405 - Probability and Statistics

**Group:** Pedro Henrique Gimenez, [Beatriz Repette](https://github.com/beatriz-repette), [Diego Meditsch](https://github.com/DMeditsch) and [Tom Hunt](https://github.com/tmphnt)

Both projects analyze the public collection of the Metropolitan Museum of Art (MET), restricted to paintings and sculptures: we started from about 480 thousand pieces and kept 15,124 works. [Trabalho 1](Trabalho%201) is the exploratory analysis and [Trabalho 2](Trabalho%202) is statistical inference over the same data. Each one has the report in `documento`, the code in `codigos`, the data in `data` and the plots in `imagens`.

## Trabalho 1: exploratory analysis

The works described by material, culture, period and popularity (the museum's Is Highlight flag), with descriptive statistics and plots crossing those variables.

| File | What it is |
|------|------------|
| [documento/trabalho1.pdf](Trabalho%201/documento/trabalho1.pdf) | Final report, with the LaTeX source alongside it. |
| [codigos/variaveis](Trabalho%201/codigos/variaveis) | Python scripts that summarize each variable. |
| [codigos/combinacao](Trabalho%201/codigos/combinacao) | R scripts for the plots that cross variables: pareto, violin, pie and density. |
| [imagens](Trabalho%201/imagens) | Generated plots. |
| [tabela_met.csv](Trabalho%201/tabela_met.csv) | Raw base exported from the MET. |

## Trabalho 2: statistical inference

Four hypotheses tested: the mean area of highlighted paintings against the non-highlighted ones, the proportion of religious themes among highlights, the correlation between year and popularity, and the regression of a sculpture's volume on its year of creation.

| File | What it is |
|------|------------|
| [documento/trabalho2.pdf](Trabalho%202/documento/trabalho2.pdf) | Final report, with the LaTeX source alongside it. |
| [codigos](Trabalho%202/codigos) | Python and R scripts for the hypothesis tests and data treatment. |
| [data](Trabalho%202/data) | Treated MET CSVs, with a README explaining the two formats. |
| [imagens/regressao_linear.png](Trabalho%202/imagens/regressao_linear.png) | Linear regression plot. |

[Aulas/regressao.py](Aulas/regressao.py) is a Pearson correlation and regression exercise done in class, outside the two projects.
