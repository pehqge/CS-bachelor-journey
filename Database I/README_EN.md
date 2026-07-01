[<kbd><img title="Português" alt="Português" src="https://flagicons.lipis.dev/flags/4x3/br.svg" width="22"></kbd> Versão em português](README.md)

# INE5423 - Database I

This is the final project for the course: modeling a database for a private school. I built it in the same order a real database is designed. It starts at the data requirements and ends with the SQL code running. Each step has its own document, so you can read it from start to finish.

The domain covers students, guardians, staff, subjects, classes, groups, rooms, tuition and class council meetings.

Team: Breno da Silva Pereira, Caio César Aquino, João Vitor Curcio Sutter, João Pedro Tamburo Faraoni and Pedro Henrique Gimenez.

## Structure

| Folder | What it holds |
|---|---|
| [Trabalho Final/](Trabalho%20Final) | The database project, from the modeling stages to the SQL code. |
| [Exercícios/](Exercícios) | SQL exercises done across the semester. |

## Final project (Trabalho Final)

The stages follow the order in which a database is designed.

| Stage | File | What it holds |
|---|---|---|
| 1. Data requirements | [1. Requisitos de Dados.pdf](Trabalho%20Final/1.%20Requisitos%20de%20Dados.pdf) | Text describing the school domain and the rules the database must follow. |
| 2. Conceptual modeling | [2. Modelagem Conceitual.pdf](Trabalho%20Final/2.%20Modelagem%20Conceitual.pdf) | The entity-relationship model: entities, attributes, relationships and cardinalities. |
| 3. Logical modeling | [3. Modelagem Lógica.pdf](Trabalho%20Final/3.%20Modelagem%20Lógica.pdf) | The relational schema derived from the conceptual model, with primary and foreign keys. |
| Early requirements draft | [Requisitos de Dados (versão inicial).pdf](Trabalho%20Final/Requisitos%20de%20Dados%20%28versão%20inicial%29.pdf) | The first delivered version of the requirements, before we expanded the domain. |

### SQL code

| File | What it does |
|---|---|
| [01_schema.sql](Trabalho%20Final/Código/01_schema.sql) | Creates the 11 tables with keys and `CHECK` constraints. Tables: sala, disciplina, funcionario, responsavel, professor, turma, aluno, aula, conselho_classe, parentesco and mensalidade. |
| [02_sample_data.sql](Trabalho%20Final/Código/02_sample_data.sql) | Inserts sample data to test the schema. |

To run it (PostgreSQL): create a database and run the schema, then the data.

```bash
psql -d my_database -f "Trabalho Final/Código/01_schema.sql"
psql -d my_database -f "Trabalho Final/Código/02_sample_data.sql"
```

## Exercises (Exercícios)

SQL exercises done across the semester. The domain here is a hospital, separate from the school final project.

| Exercise | File | Topic |
|---|---|---|
| SQL 2 | [ex2-BD.txt](Exercícios/SQL%202%20-%20Atualização%20de%20dados/ex2-BD.txt) | Table creation and data updates (`INSERT`, `UPDATE`, `DELETE`). |
| SQL 3 | [Popular.sql](Exercícios/SQL%203%20-%20Consultas%20básicas/Popular.sql) | Basic queries (`SELECT` with `WHERE`). |
| SQL 4 | [SQLite.1.sql](Exercícios/SQL%204%20-%20Junções/SQLite.1.sql) | Queries with joins (`JOIN`). |
| SQL 6 | [Subconsultas-II.sql](Exercícios/SQL%206%20-%20Subconsultas/Subconsultas-II.sql) | Subqueries with `EXISTS` and `IN`. |
| SQL 7 | [Popular.2.sql](Exercícios/SQL%207%20-%20ORDER%20BY%20e%20GROUP%20BY/Popular.2.sql) | Update from a query, `ORDER BY` and `GROUP BY`. |
| SQL 9 | [PostgreSQL SQL Online AiDE.sql](Exercícios/SQL%209%20-%20Visões/PostgreSQL%20SQL%20Online%20AiDE.sql) | Views (`CREATE VIEW`). |
