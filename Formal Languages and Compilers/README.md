[<kbd><img title="English" alt="English" src="https://flagicons.lipis.dev/flags/4x3/us.svg" width="22"></kbd> English version](README_EN.md)

# INE5421 - Linguagens Formais e Compiladores

## Gerador de Analisador Léxico e Sintático

**Estudantes:** Leonardo de Sousa Marques, Pedro Henrique Gimenez e Thayse Estevo Teixeira  
**Disciplina:** Linguagens Formais e Compiladores (INE5421/UFSC)

## Descrição

Sistema completo para análise léxica e sintática. Permite definir expressões regulares para análise léxica, gramáticas livres de contexto para análise sintática SLR, visualizar autômatos e tabelas de parsing, e realizar análise completa de código fonte.

## Funcionalidades

### Análise Léxica
- **Definição de Expressões Regulares**: Entrada no formato `nome: ER` com suporte a referências
- **Conversão para AFD**: Conversão automática de ER para autômatos finitos determinísticos
- **União e Determinização**: União via ε-transições e determinização automática
- **Minimização**: Remoção de estados inalcançáveis e equivalentes
- **Visualização**: Tabelas de transições e diagramas de autômatos
- **Exportação JFLAP**: Exportação para formato `.jff`
- **Análise Léxica**: Processamento de lexemas e geração de tokens `<lexema, tipo>`

### Análise Sintática
- **Gramáticas Livres de Contexto**: Entrada de gramáticas no formato `<S> ::= <A> | b`
- **Parser SLR**: Construção automática de tabelas ACTION/GOTO
- **Visualização LR(0)**: Diagrama da coleção canônica de itens LR(0)
- **Análise Sintática**: Parsing de tokens com histórico completo

## Estrutura do Projeto

```
src/
├── main.py                      # Ponto de entrada
├── controller/
│   └── controller.py            # Controlador MVC
├── view/
│   ├── main.ui                  # Interface gráfica (Qt Designer)
│   └── view.py                  # View
└── model/
    ├── automata/
    │   └── automaton.py         # Classe Automaton
    ├── regex/
    │   ├── converter.py         # Conversor ER → AFD
    │   ├── regular_expression.py
    │   └── syntax_tree.py
    ├── grammar/
    │   ├── cfg.py               # Gramáticas livres de contexto
    │   └── symbol_table.py      # Tabela de símbolos
    └── parser/
        └── slr.py               # Parser SLR
```

## Requisitos

- Python 3.x
- PyQt6 6.10.0
- Graphviz (para visualização de diagramas)

## Instalação

### Opção 1: Usando Makefile (recomendado)

```bash
make setup
source venv/bin/activate #ou venv\Scripts\activate, para Windows.
```

Isso instala Graphviz, cria ambiente virtual e instala dependências Python.

### Opção 2: Manual

```bash
# Instalar Graphviz
# macOS: brew install graphviz
# Linux: sudo apt install graphviz
# Windows: winget install Graphviz.Graphviz

# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
# macOS/Linux: source venv/bin/activate
# Windows: venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

## Execução

```bash
cd src
python main.py
```

## Interface do Usuário

A interface possui 5 abas principais:

1. **Regex**: Definição e processamento de expressões regulares
2. **Automata**: Visualização e exportação de autômatos finitos
3. **Analysis**: Análise léxica de código fonte
4. **SLR**: Definição de gramáticas e análise sintática
5. **Syntax**: Parsing sintático de tokens

## Exemplo de Uso

### Análise Léxica

1. **Definir Expressões Regulares** (aba Regex):
   ```
   digit: [0-9]
   num: digit.digit*
   id: [a-z].[a-z0-9]*
   ```

2. **Processar**: Gera autômatos e tabela de análise léxica

3. **Analisar Código** (aba Analysis): Inserir lexemas e gerar tokens

### Análise Sintática

1. **Definir Gramática** (aba SLR):
   ```
   <S> ::= <S> or <A> | <A>
   <A> ::= <A> and <B> | <B>
   <B> ::= not <B> | ( <S> ) | true | false
   ```

2. **Construir Tabela SLR**: Gera tabelas ACTION/GOTO automaticamente

3. **Analisar Tokens** (aba Syntax): Importar tokens da análise léxica e fazer parsing

## Notações

- **ε (epsilon)**: Representado como `&`
- **Não-terminais**: Formato `<Nome>` (ex: `<S>`, `<expr>`)
- **Terminais**: Qualquer símbolo não entre `< >`
- **Tokens**: Formato `<lexema, tipo>` ou `<lexema, erro!>` para erros
- **Definições Regulares**: Formato `nome: ER`
