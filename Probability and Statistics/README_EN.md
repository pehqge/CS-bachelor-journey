[<kbd><img title="Português" alt="Português" src="https://flagicons.lipis.dev/flags/4x3/br.svg" width="22"></kbd> Versão em português](README.md)

# INE5405 - Probability and Statistics

**Group:** Pedro Henrique Gimenez, [Beatriz Repette](https://github.com/beatriz-repette), [Diego Meditsch](https://github.com/DMeditsch) and [Tom Hunt](https://github.com/tmphnt)

I studied combinatorial analysis, probability, discrete and continuous random variables, parameter estimation and hypothesis testing.

Both projects analyze the public collection of the Metropolitan Museum of Art (MET), restricted to paintings and sculptures. We started from about 480 thousand pieces and kept 15,124 works. Each project has the report (`documento`), the code (`codigos`), the data (`data`) and the plots (`imagens`).

| Folder | What it is |
|--------|------------|
| [Aulas/regressao.py](Aulas/regressao.py) | Pearson correlation and regression exercise from class. |
| [Trabalho 1](Trabalho%201) | Exploratory analysis of the MET collection. |
| [Trabalho 2](Trabalho%202) | Statistical inference over the same data. |

## Project 1: exploratory analysis

We described the works by material, culture, period and popularity (the museum's Is Highlight flag), using descriptive statistics and plots that cross these variables.

| File | What it is |
|------|------------|
| [documento/trabalho1.pdf](Trabalho%201/documento/trabalho1.pdf) | Final report. |
| [documento/trabalho1.tex](Trabalho%201/documento/trabalho1.tex) | LaTeX source of the report. |
| [codigos/variaveis](Trabalho%201/codigos/variaveis) | Python scripts that summarize each variable. |
| [codigos/combinacao](Trabalho%201/codigos/combinacao) | R scripts for the plots that cross variables (pareto, violin, pie, density). |
| [imagens](Trabalho%201/imagens) | Generated plots. |
| [tabela_met.csv](Trabalho%201/tabela_met.csv) | Raw base exported from the MET. |
| [tarefas.md](Trabalho%201/tarefas.md) | List of planned variables and plots. |

## Project 2: statistical inference

We tested four hypotheses on the data: the mean area of highlighted paintings against the non-highlighted ones, the proportion of religious themes among highlights, the correlation between year and popularity, and the regression of a sculpture's volume on its year of creation.

| File | What it is |
|------|------------|
| [documento/trabalho2.pdf](Trabalho%202/documento/trabalho2.pdf) | Final report. |
| [documento/trabalho2.tex](Trabalho%202/documento/trabalho2.tex) | LaTeX source of the report. |
| [codigos](Trabalho%202/codigos) | Python and R scripts for the hypothesis tests and data treatment. |
| [data](Trabalho%202/data) | Treated MET CSVs, with a README explaining the two formats. |
| [imagens/regressao_linear.png](Trabalho%202/imagens/regressao_linear.png) | Linear regression plot. |
