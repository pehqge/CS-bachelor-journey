-------------- ORDER BY / GROUP BY --------------
-- 1) Os dados de todos os funcionários ordenados pelo salário (desc) e idade (asc).
--    Buscar apenas os três primeiros nessa ordem.
SELECT *
FROM Funcionarios
ORDER BY salario DESC, idade ASC
LIMIT 3;

-- 2) Nome dos médicos e o número e andar do ambulatório onde atendem,
--    ordenado pelo número do ambulatório.
SELECT m.nome, a.nroa, a.andar
FROM Medicos m
JOIN Ambulatorios a ON a.nroa = m.nroa
ORDER BY a.nroa;

-- 3) Andares dos ambulatórios e a capacidade total por andar.
SELECT a.andar, SUM(a.capacidade) AS capacidade_total
FROM Ambulatorios a
GROUP BY a.andar
ORDER BY a.andar;

-- 4) Andares dos ambulatórios cuja média de capacidade no andar seja >= 40.
SELECT a.andar
FROM Ambulatorios a
GROUP BY a.andar
HAVING AVG(a.capacidade) >= 40
ORDER BY a.andar;

-- 5) Nome dos médicos que possuem mais de uma consulta marcada.
SELECT m.nome
FROM Medicos m
JOIN Consultas c ON c.codm = m.codm
GROUP BY m.codm, m.nome
HAVING COUNT(*) > 1
ORDER BY m.nome;


-------------- ATUALIZAÇÕES --------------
-- 6) Excluir os ambulatórios que não possuem médicos atendendo neles.
DELETE FROM Ambulatorios
WHERE NOT EXISTS (
  SELECT *
  FROM Medicos m
  WHERE m.nroa = Ambulatorios.nroa
);

-- 7) O médico Pedro passa a residir na mesma cidade do paciente Paulo
--    e sua idade passa a ser o dobro da idade da paciente Ana.
UPDATE Medicos
SET cidade = (
      SELECT p.cidade
      FROM Pacientes p
      WHERE p.nome = 'Paulo'
    ),
    idade = 2 * (
      SELECT p.idade
      FROM Pacientes p
      WHERE p.nome = 'Ana'
    )
WHERE nome = 'Pedro';

-- 8) O funcionário Caio (codf = 3) tornou-se médico.
--    Especialidade = mesma da médica Maria (codm = 2)
--    e vai atender no mesmo ambulatório dela.
--    Inserir Caio na tabela Medicos aproveitando os dados em comum.
INSERT INTO Medicos (codm, nome, idade, especialidade, CPF, cidade, nroa)
SELECT
  (SELECT MAX(codm) + 1 FROM Medicos)              AS codm,
  f.nome,
  f.idade,
  m.especialidade,
  f.CPF,
  f.cidade,
  m.nroa
FROM Funcionarios f
JOIN Medicos m ON m.codm = 2
WHERE f.codf = 3;