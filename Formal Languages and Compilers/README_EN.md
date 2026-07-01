[<kbd><img title="Português" alt="Português" src="https://flagicons.lipis.dev/flags/4x3/br.svg" width="22"></kbd> Versão em português](README.md)

# INE5421 - Formal Languages and Compilers

## Lexical and syntactic analyzer generator

Students: Leonardo de Sousa Marques, Pedro Henrique Gimenez and Thayse Estevo Teixeira.

A GUI program for lexical and syntactic analysis. You can define regular expressions for the lexical part, context-free grammars for SLR syntactic analysis, view the automata and parsing tables, and analyze source code end to end.

Original repository: [leonardosm14/GALS-INE5421](https://github.com/leonardosm14/GALS-INE5421)

## What it does

Lexical analysis:

- Regular definitions in the `name: RE` format, with references.
- Conversion from RE to a deterministic finite automaton (DFA).
- Union via ε-transitions and automatic determinization.
- Minimization (removes unreachable and equivalent states).
- Transition tables and automata diagrams.
- JFLAP (`.jff`) export.
- Token generation in the `<lexeme, type>` format.

Syntactic analysis:

- Context-free grammars in the `<S> ::= <A> | b` format.
- SLR parser with automatic ACTION/GOTO table construction.
- LR(0) canonical collection diagram.
- Token parsing with full history.

## Structure

| Folder / File | What it holds |
|---|---|
| [src/](src) | Source code, organized as MVC. |
| [docs/](docs) | Assignment briefs and documentation. |
| [inputs/](inputs) | Example inputs (regular expressions and grammars). |
| [Makefile](Makefile) | Setup: installs Graphviz, creates the venv and installs dependencies. |
| [requirements.txt](requirements.txt) | Python dependencies (PyQt6 and graphviz). |

### Code (`src/`)

| File | What it holds |
|---|---|
| [main.py](src/main.py) | Entry point. |
| [controller/controller.py](src/controller/controller.py) | Controller (MVC). |
| [view/view.py](src/view/view.py) | The view. |
| [view/main.ui](src/view/main.ui) | GUI layout (Qt Designer). |
| [view/automata_image_dialog.py](src/view/automata_image_dialog.py) | Dialog that shows the automaton image. |
| [view/utils/zoomable_graphics_view.py](src/view/utils/zoomable_graphics_view.py) | Zoomable viewer. |
| [model/automata/automaton.py](src/model/automata/automaton.py) | Automaton class. |
| [model/regex/converter.py](src/model/regex/converter.py) | RE to DFA converter. |
| [model/regex/regular_expression.py](src/model/regex/regular_expression.py) | Regular expression. |
| [model/regex/syntax_tree.py](src/model/regex/syntax_tree.py) | RE syntax tree. |
| [model/grammar/cfg.py](src/model/grammar/cfg.py) | Context-free grammars. |
| [model/grammar/symbol_table.py](src/model/grammar/symbol_table.py) | Symbol table. |
| [model/parser/slr.py](src/model/parser/slr.py) | SLR parser. |

### Documentation (`docs/`)

| File | What it holds |
|---|---|
| [documentation.pdf](docs/documentation.pdf) | Project documentation. |
| [Trabalho 1 - Requisitos.pdf](docs/Trabalho%201%20-%20Requisitos.pdf) | Assignment 1 brief. |
| [Trabalho 2 - Requisitos.pdf](docs/Trabalho%202%20-%20Requisitos.pdf) | Assignment 2 brief. |

### Example inputs (`inputs/`)

| Folder | What it holds |
|---|---|
| [regular expressions/](inputs/regular%20expressions) | Sample regular definitions and test sentences. |
| [grammars/](inputs/grammars) | Sample grammars. |

## Install

You need Python 3, PyQt6 and Graphviz. The fastest way is the Makefile:

```bash
make setup
source venv/bin/activate   # on Windows: venv\Scripts\activate
```

That installs Graphviz, creates the virtual environment and installs the dependencies.

## Run

```bash
cd src
python main.py
```

## Notation

- `&` stands for ε (epsilon).
- Non-terminals in the `<Name>` format (e.g. `<S>`, `<expr>`).
- Terminals: any symbol outside `< >`.
- Tokens in the `<lexeme, type>` format (or `<lexeme, erro!>` for errors).
- Regular definitions in the `name: RE` format.
