[<kbd><img title="English" alt="English" src="https://flagicons.lipis.dev/flags/4x3/us.svg" width="22"></kbd> English version](README_EN.md)

# INE5421 - Linguagens Formais e Compiladores

**Equipe:** Leonardo de Sousa Marques, Pedro Henrique Gimenez e Thayse Estevo Teixeira

Um gerador de analisador léxico e sintático com interface gráfica em PyQt6. Recebe expressões regulares para a parte léxica e gramáticas livres de contexto para a análise sintática SLR, mostra os autômatos e as tabelas de parsing e analisa um código fonte do começo ao fim. Repositório original: [leonardosm14/GALS-INE5421](https://github.com/leonardosm14/GALS-INE5421).

## O que ele faz

Análise léxica:

- Definições regulares no formato `nome: ER`, com referências.
- Conversão de ER para autômato finito determinístico, união por ε-transições e determinização automática.
- Minimização, removendo estados inalcançáveis e equivalentes.
- Tabelas de transição, diagramas dos autômatos e exportação para JFLAP (`.jff`).
- Geração de tokens no formato `<lexema, tipo>`.

Análise sintática:

- Gramáticas livres de contexto no formato `<S> ::= <A> | b`.
- Parser SLR com construção automática das tabelas ACTION e GOTO.
- Diagrama da coleção canônica de itens LR(0).
- Parsing de tokens com histórico completo.

## Estrutura

| Pasta / Arquivo | O que tem |
|---|---|
| [src/](src) | Código-fonte em MVC: `model/` com autômatos, expressões regulares e gramáticas, `view/` com a interface Qt e `controller/` ligando os dois. |
| [docs/](docs) | [Documentação do projeto](docs/documentation.pdf) e os enunciados dos dois trabalhos. |
| [inputs/](inputs) | Exemplos de entrada: definições regulares com sentenças de teste e gramáticas. |
| [Makefile](Makefile) | Instala o Graphviz, cria o venv e instala as dependências. |
| [requirements.txt](requirements.txt) | Dependências Python: PyQt6 e graphviz. |

## Como rodar

Precisa de Python 3, PyQt6 e Graphviz. O Makefile resolve tudo:

```bash
make setup
source venv/bin/activate   # no Windows: venv\Scripts\activate
cd src && python main.py
```

## Notações

- `&` representa ε (epsilon).
- Não-terminais no formato `<Nome>` (ex: `<S>`, `<expr>`).
- Terminais: qualquer símbolo fora de `< >`.
- Tokens no formato `<lexema, tipo>`, ou `<lexema, erro!>` para erros.
- Definições regulares no formato `nome: ER`.
