[<kbd><img title="English" alt="English" src="https://flagicons.lipis.dev/flags/4x3/us.svg" width="22"></kbd> English version](README_EN.md)

# INE5423 - Banco de Dados I

Aqui está o trabalho final da disciplina: a modelagem de um banco de dados para uma escola particular. Fizemos na mesma ordem em que um banco real é projetado. Começa nos requisitos de dados e termina no código SQL rodando. Cada etapa tem seu próprio documento, então dá para ler do começo ao fim.

O domínio cobre alunos, responsáveis, funcionários, disciplinas, aulas, turmas, salas, mensalidades e reuniões de conselho de classe.

Equipe: Breno da Silva Pereira, Caio César Aquino, João Vitor Curcio Sutter, João Pedro Tamburo Faraoni e Pedro Henrique Gimenez.

## Estrutura

| Pasta | O que tem |
|---|---|
| [Trabalho Final/](Trabalho%20Final) | O projeto do banco de dados, das etapas de modelagem ao código SQL. |
| [Exercícios/](Exercícios) | Exercícios de SQL feitos ao longo do semestre. |

## Trabalho Final

As etapas seguem a ordem de projeto de um banco de dados.

| Etapa | Arquivo | O que tem |
|---|---|---|
| 1. Requisitos de dados | [1. Requisitos de Dados.pdf](Trabalho%20Final/1.%20Requisitos%20de%20Dados.pdf) | Texto que descreve o domínio da escola e as regras que o banco precisa seguir. |
| 2. Modelagem conceitual | [2. Modelagem Conceitual.pdf](Trabalho%20Final/2.%20Modelagem%20Conceitual.pdf) | O modelo entidade-relacionamento: entidades, atributos, relacionamentos e cardinalidades. |
| 3. Modelagem lógica | [3. Modelagem Lógica.pdf](Trabalho%20Final/3.%20Modelagem%20Lógica.pdf) | O esquema relacional derivado do modelo conceitual, com chaves primárias e estrangeiras. |
| Versão inicial dos requisitos | [Requisitos de Dados (versão inicial).pdf](Trabalho%20Final/Requisitos%20de%20Dados%20%28versão%20inicial%29.pdf) | A primeira versão entregue dos requisitos, antes de expandirmos o domínio. |

### Código SQL

| Arquivo | O que faz |
|---|---|
| [01_schema.sql](Trabalho%20Final/Código/01_schema.sql) | Cria as 11 tabelas com chaves e restrições `CHECK`. Tabelas: sala, disciplina, funcionario, responsavel, professor, turma, aluno, aula, conselho_classe, parentesco e mensalidade. |
| [02_sample_data.sql](Trabalho%20Final/Código/02_sample_data.sql) | Insere dados de exemplo para testar o esquema. |

Para rodar (PostgreSQL): crie um banco e execute o schema e depois os dados.

```bash
psql -d meu_banco -f "Trabalho Final/Código/01_schema.sql"
psql -d meu_banco -f "Trabalho Final/Código/02_sample_data.sql"
```

## Exercícios

Exercícios de SQL feitos ao longo do semestre. O domínio é um hospital, separado do trabalho final da escola.

| Exercício | Arquivo | Tema |
|---|---|---|
| SQL 2 | [ex2-BD.txt](Exercícios/SQL%202%20-%20Atualização%20de%20dados/ex2-BD.txt) | Criação de tabelas e atualização de dados (`INSERT`, `UPDATE`, `DELETE`). |
| SQL 3 | [Popular.sql](Exercícios/SQL%203%20-%20Consultas%20básicas/Popular.sql) | Consultas básicas (`SELECT` com `WHERE`). |
| SQL 4 | [SQLite.1.sql](Exercícios/SQL%204%20-%20Junções/SQLite.1.sql) | Consultas com junções (`JOIN`). |
| SQL 6 | [Subconsultas-II.sql](Exercícios/SQL%206%20-%20Subconsultas/Subconsultas-II.sql) | Subconsultas com `EXISTS` e `IN`. |
| SQL 7 | [Popular.2.sql](Exercícios/SQL%207%20-%20ORDER%20BY%20e%20GROUP%20BY/Popular.2.sql) | Atualização com consulta, `ORDER BY` e `GROUP BY`. |
| SQL 9 | [PostgreSQL SQL Online AiDE.sql](Exercícios/SQL%209%20-%20Visões/PostgreSQL%20SQL%20Online%20AiDE.sql) | Visões (`CREATE VIEW`). |
