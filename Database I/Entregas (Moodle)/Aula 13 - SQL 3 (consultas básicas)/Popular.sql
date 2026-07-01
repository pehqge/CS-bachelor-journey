-- 1.  Buscar os dados dos médicos com menos de 40 anos ou com especialidade diferente de traumatologia
SELECT * FROM Medicos WHERE idade < 40 OR especialidade != 'traumatologia';

-- 2. Buscar o nome e a idade dos pacientes que não residem em Florianópolis
SELECT nome, idade from Pacientes where cidade != 'Florianopolis';

-- 3. Buscar o nome e a idade (em meses) dos pacientes
SELECT nome, idade*12 as idade_meses from Pacientes;

-- 4. Qual o horário da última consulta marcada para o dia 13/10/2020?
select max(hora) from Consultas where data = '2020/10/13';

-- 5. Qual a média de idade dos médicos e o total de ambulatórios atendidos por eles?
select avg(idade) as media_idade, COUNT(DISTINCT nroa) as total_nroa from Medicos;

-- 6. Buscar o código, o nome e o salário líquido dos funcionários. O salário líquido é o salário cadastrado menos 20%
SELECT codf, nome, salario*0.8 as salario_liquido from Funcionarios;

-- 7. Buscar o nome dos funcionários que terminam com a letra 'a'
select nome from Funcionarios where nome like '%a';

-- 8. Buscar o nome e a especialidade dos médicos cuja segunda e a última letra de seus nomes seja a letra 'o'
select nome, especialidade from medicos 
where nome like '_o%o';

-- 9. Buscar os códigos e nomes dos pacientes com mais de 25 anos que estão com tendinite, fratura, gripe ou sarampo 
select codp, nome from Pacientes 
where idade > 25 
and doenca in ('tendinite', 'fratura', 'gripe', 'sarampo');

-- 10. Buscar os CPFs, nomes e idades de todas as pessoas (médicos, pacientes ou funcionários) que residem em Florianópolis
select cpf, nome, idade from Medicos where cidade = 'Florianopolis' 
union select cpf, nome, idade from Pacientes where cidade = 'Florianopolis' 
UNION select cpf, nome, idade from Funcionarios where cidade = 'Florianopolis';