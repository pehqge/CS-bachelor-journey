[<kbd><img title="Português" alt="Português" src="https://flagicons.lipis.dev/flags/4x3/br.svg" width="22"></kbd> Versão em português](README_PT.md)

# INE5421 - Formal Languages and Compilers

## Lexical and Syntactic Analyzer Generator

**Students:** Leonardo de Sousa Marques, Pedro Henrique Gimenez and Thayse Estevo Teixeira

A complete system for lexical and syntactic analysis. It lets you define regular expressions for lexical analysis, context-free grammars for SLR syntactic analysis, visualize automata and parsing tables, and run a full analysis over source code.

### Lexical Analysis
- Regular expression definitions in the `name: RE` format, with references
- Automatic conversion from RE to deterministic finite automata (DFA)
- Union via ε-transitions and automatic determinization
- Minimization (removal of unreachable and equivalent states)
- Transition tables and automata diagrams
- JFLAP (`.jff`) export
- Lexeme processing and `<lexeme, type>` token generation

### Syntactic Analysis
- Context-free grammars in the `<S> ::= <A> | b` format
- SLR parser with automatic ACTION/GOTO table construction
- LR(0) canonical collection diagram
- Token parsing with full history

Built in Python with PyQt6 and Graphviz. See [README_PT.md](README_PT.md) for build and usage instructions.

Original repository: [leonardosm14/GALS-INE5421](https://github.com/leonardosm14/GALS-INE5421)
