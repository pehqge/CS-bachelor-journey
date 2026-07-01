[<kbd><img title="English" alt="English" src="https://flagicons.lipis.dev/flags/4x3/us.svg" width="22"></kbd> English version](README_EN.md)

# INE5421 - Linguagens Formais e Compiladores

## Gerador de analisador léxico e sintático

Estudantes: Leonardo de Sousa Marques, Pedro Henrique Gimenez e Thayse Estevo Teixeira.

Um programa com interface gráfica para análise léxica e sintática. Dá para definir expressões regulares para a parte léxica, gramáticas livres de contexto para a análise sintática SLR, ver os autômatos e as tabelas de parsing, e analisar um código fonte do começo ao fim.

Repositório original: [leonardosm14/GALS-INE5421](https://github.com/leonardosm14/GALS-INE5421)

## O que ele faz

Análise léxica:

- Definições regulares no formato `nome: ER`, com referências.
- Conversão de ER para autômato finito determinístico (AFD).
- União por ε-transições e determinização automática.
- Minimização (remove estados inalcançáveis e equivalentes).
- Tabelas de transição e diagramas dos autômatos.
- Exportação para JFLAP (`.jff`).
- Geração de tokens no formato `<lexema, tipo>`.

Análise sintática:

- Gramáticas livres de contexto no formato `<S> ::= <A> | b`.
- Parser SLR com construção automática das tabelas ACTION/GOTO.
- Diagrama da coleção canônica de itens LR(0).
- Parsing de tokens com histórico completo.

## Estrutura

| Pasta / Arquivo | O que tem |
|---|---|
| [src/](src) | Código-fonte, organizado em MVC. |
| [docs/](docs) | Enunciados e documentação. |
| [inputs/](inputs) | Exemplos de entrada (ERs e gramáticas). |
| [Makefile](Makefile) | Setup: instala Graphviz, cria o venv e instala as dependências. |
| [requirements.txt](requirements.txt) | Dependências Python (PyQt6 e graphviz). |

### Código (`src/`)

| Arquivo | O que tem |
|---|---|
| [main.py](src/main.py) | Ponto de entrada. |
| [controller/controller.py](src/controller/controller.py) | Controlador (MVC). |
| [view/view.py](src/view/view.py) | A view. |
| [view/main.ui](src/view/main.ui) | Interface gráfica (Qt Designer). |
| [view/automata_image_dialog.py](src/view/automata_image_dialog.py) | Diálogo que mostra a imagem do autômato. |
| [view/utils/zoomable_graphics_view.py](src/view/utils/zoomable_graphics_view.py) | Visualizador com zoom. |
| [model/automata/automaton.py](src/model/automata/automaton.py) | Classe do autômato. |
| [model/regex/converter.py](src/model/regex/converter.py) | Conversor de ER para AFD. |
| [model/regex/regular_expression.py](src/model/regex/regular_expression.py) | Expressão regular. |
| [model/regex/syntax_tree.py](src/model/regex/syntax_tree.py) | Árvore de sintaxe da ER. |
| [model/grammar/cfg.py](src/model/grammar/cfg.py) | Gramáticas livres de contexto. |
| [model/grammar/symbol_table.py](src/model/grammar/symbol_table.py) | Tabela de símbolos. |
| [model/parser/slr.py](src/model/parser/slr.py) | Parser SLR. |

### Documentação (`docs/`)

| Arquivo | O que tem |
|---|---|
| [documentation.pdf](docs/documentation.pdf) | Documentação do projeto. |
| [Trabalho 1 - Requisitos.pdf](docs/Trabalho%201%20-%20Requisitos.pdf) | Enunciado do Trabalho 1. |
| [Trabalho 2 - Requisitos.pdf](docs/Trabalho%202%20-%20Requisitos.pdf) | Enunciado do Trabalho 2. |

### Entradas de exemplo (`inputs/`)

| Pasta | O que tem |
|---|---|
| [regular expressions/](inputs/regular%20expressions) | Exemplos de definições regulares e sentenças de teste. |
| [grammars/](inputs/grammars) | Exemplos de gramáticas. |

## Como instalar

Precisa de Python 3, PyQt6 e Graphviz. O jeito mais rápido é o Makefile:

```bash
make setup
source venv/bin/activate   # no Windows: venv\Scripts\activate
```

Isso instala o Graphviz, cria o ambiente virtual e instala as dependências.

## Como rodar

```bash
cd src
python main.py
```

## Notações

- `&` representa ε (epsilon).
- Não-terminais no formato `<Nome>` (ex: `<S>`, `<expr>`).
- Terminais: qualquer símbolo fora de `< >`.
- Tokens no formato `<lexema, tipo>` (ou `<lexema, erro!>` para erros).
- Definições regulares no formato `nome: ER`.
