-- 1. Criar visão dos funcionários de Florianopolis com mais de 40 anos (com WITH CHECK OPTION)
CREATE VIEW FuncFpolis40 (codigo, nome, CPF, idade) AS
SELECT f.codf, f.nome, f.CPF, f.idade
FROM Funcionarios f
WHERE f.cidade = 'Florianopolis' AND f.idade > 40
WITH CHECK OPTION;

-- 2. Consultar os dados da visão (esperado inicialmente: apenas Caio)
SELECT * FROM FuncFpolis40;

-- 3. Inserir Francisco (cod=9, CPF=33300033333, idade=38) via visão (esperado: REJEITADA pelo WITH CHECK OPTION)
INSERT INTO FuncFpolis40 (codigo, nome, CPF, idade)
VALUES (9, 'Francisco', 33300033333, 38);

-- 4. Inserir Rodrigo (cod=10, CPF=22200022233, idade=41) via visão (esperado: REJEITADA pois o predicado exige cidade='Florianopolis' e a visão não tem esse atributo)
INSERT INTO FuncFpolis40 (codigo, nome, CPF, idade)
VALUES (10, 'Rodrigo', 22200022233, 41);

-- 5. Consultar a visão após as inserções acima (esperado: NÃO aparece Rodrigo/Francisco, segue somente Caio)
SELECT * FROM FuncFpolis40;

-- 6. Trigger INSTEAD OF para inserir diretamente em Funcionarios com cidade='Florianopolis' ao invés de inserir na visão
DROP TRIGGER IF EXISTS InsercaoFuncFpolis ON FuncFpolis40;
DROP FUNCTION IF EXISTS inserir_funcfpolis40();

CREATE OR REPLACE FUNCTION inserir_funcfpolis40()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
  INSERT INTO Funcionarios (codf, nome, idade, CPF, cidade, salario)
  VALUES (NEW.codigo, NEW.nome, NEW.idade, NEW.CPF, 'Florianopolis', 0);
  RETURN NULL; -- em INSTEAD OF, o retorno é ignorado
END;
$$;

CREATE TRIGGER InsercaoFuncFpolis
INSTEAD OF INSERT ON FuncFpolis40
FOR EACH ROW
EXECUTE FUNCTION inserir_funcfpolis40();

-- 7. Inserir Raul (cod=11, CPF=44400044433, idade=53) via visão (esperado: ACEITA pela trigger e satisfaz o predicado da visão)
INSERT INTO FuncFpolis40 (codigo, nome, CPF, idade)
VALUES (11, 'Raul', 44400044433, 53);

-- 8. Consultar a visão após a trigger (esperado: Caio e Raul visíveis)
SELECT * FROM FuncFpolis40;