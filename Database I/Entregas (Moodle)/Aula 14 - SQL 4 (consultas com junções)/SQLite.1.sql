----------- não natural --------------
-- 1. Buscar o nome e CPF dos médicos que também são pacientes do hospital
SELECT Medicos.nome, Medicos.CPF from Medicos join Pacientes on Medicos.CPF = Pacientes.CPF;

-- 2. Buscar nomes de funcionários e de médicos (exibir pares de nomes) que residem na mesma cidade
SELECT Medicos.nome, Funcionarios.nome from Medicos JOIN Funcionarios on Medicos.cidade = Funcionarios.cidade;

-- 3. Buscar o nome e idade dos médicos que têm consulta marcada com a paciente cujo nome é Ana
select Medicos.nome, Medicos.idade from Medicos 
join Consultas on Medicos.codm = Consultas.codm 
join Pacientes on Consultas.codp = Pacientes.codp where Pacientes.nome = 'Ana';

-- 4. Buscar o número dos ambulatórios que estão no mesmo andar do ambulatório 5 
SELECT a2.nroa from Ambulatorios a1 join Ambulatorios a2 on a1.andar = a2.andar  where a1.nroa = 5;

--------- Join Natural ------------
-- 5.  Buscar o código e o nome dos pacientes com consulta marcada para horários após às 14 horas
select codp, nome from Pacientes NATURAL join Consultas where hora > '14:00';

-- 6. Buscar o número e o andar dos ambulatórios cujos médicos possuem consultas marcadas para o dia 12/10/2020
select nroa, andar from Ambulatorios natural join Medicos natural join Consultas where data = '2020/10/12';

-------- Outer Join -------------
-- 7. Buscar os dados de todos os ambulatórios e, para aqueles ambulatórios onde médicos dão atendimento, exibir também os códigos e nomes destes médicos
select Ambulatorios.*, codm, nome from Ambulatorios left join Medicos on Ambulatorios.nroa = Medicos.nroa;

-- 8. Buscar o CPF e o nome de todos os médicos e, para aqueles médicos que possuem consultas marcadas, exibir também o nome dos paciente e a data da consulta
select Medicos.CPF, Medicos.nome, Pacientes.nome, data from Medicos left join Consultas on Medicos.codm = Consultas.codm join Pacientes on Consultas.codp = Pacientes.codp;