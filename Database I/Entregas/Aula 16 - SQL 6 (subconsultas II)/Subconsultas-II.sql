-------- EXISTS --------------
-- 1. Buscar o nome e o CPF dos médicos que também são pacientes do hospital
SELECT m.nome, m.cpf
FROM Medicos m
WHERE EXISTS (
  SELECT *
  FROM Pacientes p
  WHERE p.cpf = m.cpf
);

-- 2. Buscar o nome e o CPF dos médicos ortopedistas, e a data das suas consultas, para os ortopedistas que têm consulta marcada com a paciente Ana
SELECT m.nome, m.cpf, c.data
FROM Medicos m
JOIN Consultas c ON c.codm = m.codm
WHERE m.especialidade = 'ortopedia'
  AND EXISTS (
    SELECT *
    FROM Pacientes p
    JOIN Consultas cx ON cx.codm = m.codm AND cx.codp = p.codp
    WHERE p.nome = 'Ana'
  );
  
-- 3. Buscar o nome e o CPF dos médicos que têm consultas marcadas com todos os pacientes
SELECT m.nome, m.cpf
FROM Medicos m
WHERE NOT EXISTS (
  SELECT *
  FROM Pacientes p
  WHERE NOT EXISTS (
    SELECT *
    FROM Consultas c
    WHERE c.codm = m.codm AND c.codp = p.codp
  )
);

-- 4.  Buscar o nome e o CPF dos médicos ortopedistas que têm consultas marcadas com todos os pacientes de Florianópolis
SELECT m.nome, m.cpf
FROM Medicos m
WHERE m.especialidade = 'ortopedia'
  AND NOT EXISTS (
    SELECT *
    FROM Pacientes p
    WHERE p.cidade = 'Florianopolis'
      AND NOT EXISTS (
        SELECT *
        FROM Consultas c
        WHERE c.codm = m.codm AND c.codp = p.codp
      )
  );
  
 ---------------- FROM -------------------
 -- 1. Buscar a data e a hora das consultas marcadas para a médica Maria
SELECT C.data, C.hora
FROM (SELECT codm FROM Medicos WHERE nome = 'Maria') AS M
JOIN Consultas C ON C.codm = M.codm;

-- 2. Buscar o nome e a cidade dos pacientes que têm consultas marcadas com ortopedistas
SELECT DISTINCT p.nome, p.cidade
FROM (SELECT codm FROM Medicos WHERE especialidade = 'ortopedia') AS Orto
JOIN Consultas c ON c.codm = Orto.codm
JOIN Pacientes p ON p.codp = c.codp;

-- 3. Buscar o nome e o CPF dos médicos que atendem no mesmo ambulatório do médico Pedro
SELECT m.nome, m.cpf
FROM (SELECT codm, nroa FROM Medicos WHERE nome = 'Pedro') AS MP
JOIN Medicos m
  ON m.nroa = MP.nroa;