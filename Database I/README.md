[<kbd><img title="English" alt="English" src="https://flagicons.lipis.dev/flags/4x3/us.svg" width="22"></kbd> English version](README_EN.md)

# INE5423 - Banco de Dados I

**Equipe:** Breno da Silva Pereira, Caio César Aquino, João Vitor Curcio Sutter, João Pedro Tamburo Faraoni e Pedro Henrique Gimenez

O [trabalho final](Trabalho%20Final) é a modelagem de um banco de dados para uma escola particular, dos requisitos de dados até o SQL rodando. O domínio cobre alunos, responsáveis, funcionários, disciplinas, aulas, turmas, salas, mensalidades e reuniões de conselho de classe. A pasta [Exercícios](Exercícios) tem os exercícios de SQL do semestre, sobre um domínio separado.

## Trabalho final

| Etapa | Arquivo |
|---|---|
| 1. Requisitos de dados | [1. Requisitos de Dados.pdf](Trabalho%20Final/1.%20Requisitos%20de%20Dados.pdf) |
| 2. Modelagem conceitual | [2. Modelagem Conceitual.pdf](Trabalho%20Final/2.%20Modelagem%20Conceitual.pdf) |
| 3. Modelagem lógica | [3. Modelagem Lógica.pdf](Trabalho%20Final/3.%20Modelagem%20Lógica.pdf) |
| Versão inicial dos requisitos | [Requisitos de Dados (versão inicial).pdf](Trabalho%20Final/Requisitos%20de%20Dados%20%28versão%20inicial%29.pdf) |

### Código SQL

| Arquivo | O que faz |
|---|---|
| [01_schema.sql](Trabalho%20Final/Código/01_schema.sql) | Cria as 11 tabelas com chaves e restrições `CHECK`. |
| [02_sample_data.sql](Trabalho%20Final/Código/02_sample_data.sql) | Insere dados de exemplo para testar o esquema. |

Para rodar (PostgreSQL):

```bash
psql -d meu_banco -f "Trabalho Final/Código/01_schema.sql"
psql -d meu_banco -f "Trabalho Final/Código/02_sample_data.sql"
```

## Exercícios

Consultas e comandos SQL sobre um banco de hospital, um tema por lista.

| Exercício | Arquivo | Tema |
|---|---|---|
| SQL 2 | [ex2-BD.txt](Exercícios/SQL%202%20-%20Atualização%20de%20dados/ex2-BD.txt) | `INSERT`, `UPDATE`, `DELETE` |
| SQL 3 | [Popular.sql](Exercícios/SQL%203%20-%20Consultas%20básicas/Popular.sql) | `SELECT` com `WHERE` |
| SQL 4 | [SQLite.1.sql](Exercícios/SQL%204%20-%20Junções/SQLite.1.sql) | `JOIN` |
| SQL 6 | [Subconsultas-II.sql](Exercícios/SQL%206%20-%20Subconsultas/Subconsultas-II.sql) | Subconsultas com `EXISTS` e `IN` |
| SQL 7 | [Popular.2.sql](Exercícios/SQL%207%20-%20ORDER%20BY%20e%20GROUP%20BY/Popular.2.sql) | `ORDER BY` e `GROUP BY` |
| SQL 9 | [PostgreSQL SQL Online AiDE.sql](Exercícios/SQL%209%20-%20Visões/PostgreSQL%20SQL%20Online%20AiDE.sql) | `CREATE VIEW` |
