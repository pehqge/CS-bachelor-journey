[<kbd><img title="Português" alt="Português" src="https://flagicons.lipis.dev/flags/4x3/br.svg" width="22"></kbd> Versão em português](README.md)

# INE5421 - Formal Languages and Compilers

**Team:** Leonardo de Sousa Marques, Pedro Henrique Gimenez and Thayse Estevo Teixeira

A lexical and syntactic analyzer generator with a PyQt6 GUI. It takes regular expressions for the lexical part and context-free grammars for SLR syntactic analysis, shows the automata and the parsing tables, and analyzes source code end to end. Original repository: [leonardosm14/GALS-INE5421](https://github.com/leonardosm14/GALS-INE5421).

## What it does

Lexical analysis:

- Regular definitions in the `name: RE` format, with references.
- Conversion from RE to a deterministic finite automaton, union via ε-transitions and automatic determinization.
- Minimization, removing unreachable and equivalent states.
- Transition tables, automata diagrams and JFLAP (`.jff`) export.
- Token generation in the `<lexeme, type>` format.

Syntactic analysis:

- Context-free grammars in the `<S> ::= <A> | b` format.
- SLR parser with automatic ACTION and GOTO table construction.
- LR(0) canonical collection diagram.
- Token parsing with full history.

## Structure

| Folder / File | What it holds |
|---|---|
| [src/](src) | Source code in MVC: `model/` with automata, regular expressions and grammars, `view/` with the Qt interface and `controller/` wiring the two. |
| [docs/](docs) | [Project documentation](docs/documentation.pdf) and the two assignment briefs. |
| [inputs/](inputs) | Example inputs: regular definitions with test sentences, and grammars. |
| [Makefile](Makefile) | Installs Graphviz, creates the venv and installs the dependencies. |
| [requirements.txt](requirements.txt) | Python dependencies: PyQt6 and graphviz. |

## Running it

You need Python 3, PyQt6 and Graphviz. The Makefile handles all of it:

```bash
make setup
source venv/bin/activate   # on Windows: venv\Scripts\activate
cd src && python main.py
```

## Notation

- `&` stands for ε (epsilon).
- Non-terminals in the `<Name>` format (e.g. `<S>`, `<expr>`).
- Terminals: any symbol outside `< >`.
- Tokens in the `<lexeme, type>` format, or `<lexeme, erro!>` for errors.
- Regular definitions in the `name: RE` format.
