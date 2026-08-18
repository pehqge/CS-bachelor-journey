[<kbd><img title="Português" alt="Português" src="https://flagicons.lipis.dev/flags/4x3/br.svg" width="22"></kbd> Versão em português](README.md)

# INE5423 - Database I

**Team:** Breno da Silva Pereira, Caio César Aquino, João Vitor Curcio Sutter, João Pedro Tamburo Faraoni and Pedro Henrique Gimenez

The [final project](Trabalho%20Final) is the design of a database for a private school, from the data requirements to the SQL running. The domain covers students, guardians, staff, subjects, classes, groups, rooms, tuition and class council meetings. The [Exercícios](Exercícios) folder holds the semester's SQL exercises, on a separate domain.

## Final project

| Stage | File |
|---|---|
| 1. Data requirements | [1. Requisitos de Dados.pdf](Trabalho%20Final/1.%20Requisitos%20de%20Dados.pdf) |
| 2. Conceptual modeling | [2. Modelagem Conceitual.pdf](Trabalho%20Final/2.%20Modelagem%20Conceitual.pdf) |
| 3. Logical modeling | [3. Modelagem Lógica.pdf](Trabalho%20Final/3.%20Modelagem%20Lógica.pdf) |
| Early requirements draft | [Requisitos de Dados (versão inicial).pdf](Trabalho%20Final/Requisitos%20de%20Dados%20%28versão%20inicial%29.pdf) |

### SQL code

| File | What it does |
|---|---|
| [01_schema.sql](Trabalho%20Final/Código/01_schema.sql) | Creates the 11 tables with keys and `CHECK` constraints. |
| [02_sample_data.sql](Trabalho%20Final/Código/02_sample_data.sql) | Inserts sample data to test the schema. |

To run it (PostgreSQL):

```bash
psql -d my_database -f "Trabalho Final/Código/01_schema.sql"
psql -d my_database -f "Trabalho Final/Código/02_sample_data.sql"
```

## Exercises

SQL queries and statements over a hospital database, one topic per list.

| Exercise | File | Topic |
|---|---|---|
| SQL 2 | [ex2-BD.txt](Exercícios/SQL%202%20-%20Atualização%20de%20dados/ex2-BD.txt) | `INSERT`, `UPDATE`, `DELETE` |
| SQL 3 | [Popular.sql](Exercícios/SQL%203%20-%20Consultas%20básicas/Popular.sql) | `SELECT` with `WHERE` |
| SQL 4 | [SQLite.1.sql](Exercícios/SQL%204%20-%20Junções/SQLite.1.sql) | `JOIN` |
| SQL 6 | [Subconsultas-II.sql](Exercícios/SQL%206%20-%20Subconsultas/Subconsultas-II.sql) | Subqueries with `EXISTS` and `IN` |
| SQL 7 | [Popular.2.sql](Exercícios/SQL%207%20-%20ORDER%20BY%20e%20GROUP%20BY/Popular.2.sql) | `ORDER BY` and `GROUP BY` |
| SQL 9 | [PostgreSQL SQL Online AiDE.sql](Exercícios/SQL%209%20-%20Visões/PostgreSQL%20SQL%20Online%20AiDE.sql) | `CREATE VIEW` |
