/*
    Script de inserção de dados de exemplo
    Disciplina: Banco de Dados I
    Grupo: Breno da Silva Pereira, Caio César Aquino, João Vitor Curcio Sutter,
    João Pedro Tamburo Faraoni, Pedro Henrique Gimenez
*/

-- ==============================================================================
-- INSERÇÃO DE DADOS DE EXEMPLO
-- ==============================================================================

-- 1. SALAS
INSERT INTO sala (numero, andar, capacidade) VALUES
(101, 1, 30),
(102, 1, 25),
(201, 2, 35),
(202, 2, 28),
(301, 3, 40);

-- 2. DISCIPLINAS
INSERT INTO disciplina (nome, carga_horaria, ementa) VALUES
('Matemática', 80, 'Estudo de álgebra, geometria e trigonometria básica.'),
('Português', 80, 'Gramática, literatura e redação.'),
('História', 60, 'História do Brasil e história geral.'),
('Geografia', 60, 'Geografia física e humana do Brasil e do mundo.'),
('Biologia', 80, 'Estudo dos seres vivos e seus processos.'),
('Química', 80, 'Química geral e inorgânica.'),
('Física', 80, 'Mecânica, termodinâmica e eletricidade.'),
('Inglês', 60, 'Inglês básico e intermediário.');

-- 3. RESPONSÁVEIS
INSERT INTO responsavel (cpf, nome, telefone, email, endereco) VALUES
('12345678901', 'Maria Silva Santos', '(11) 98765-4321', 'maria.santos@email.com', 'Rua das Flores, 123, São Paulo - SP'),
('23456789012', 'João Oliveira Lima', '(11) 97654-3210', 'joao.lima@email.com', 'Av. Paulista, 456, São Paulo - SP'),
('34567890123', 'Ana Costa Ferreira', '(11) 96543-2109', 'ana.ferreira@email.com', 'Rua Augusta, 789, São Paulo - SP'),
('45678901234', 'Carlos Souza Alves', '(11) 95432-1098', 'carlos.alves@email.com', 'Rua Oscar Freire, 321, São Paulo - SP'),
('56789012345', 'Lucia Pereira Rocha', '(11) 94321-0987', 'lucia.rocha@email.com', 'Av. Faria Lima, 654, São Paulo - SP');

-- 4. FUNCIONÁRIOS
INSERT INTO funcionario (cpf, nome, salario, funcao, data_admissao, email_corporativo) VALUES
('11111111111', 'Prof. Roberto', 4500.00, 'Professor', '2023-01-15', 'roberto.mat@escola.edu.br'),
('22222222222', 'Profa. Carla', 4500.00, 'Professor', '2023-02-01', 'carla.port@escola.edu.br'),
('33333333333', 'Prof. Fernando', 4200.00, 'Professor', '2023-03-10', 'fernando.hist@escola.edu.br'),
('44444444444', 'Profa. Juliana', 4200.00, 'Professor', '2023-01-20', 'juliana.geo@escola.edu.br'),
('55555555555', 'Prof. André', 4800.00, 'Professor', '2022-08-15', 'andre.bio@escola.edu.br'),
('66666666666', 'Dra. Sandra', 6500.00, 'Coordenador', '2022-01-10', 'sandra.coord@escola.edu.br'),
('77777777777', 'Sr. Paulo', 8500.00, 'Diretor', '2020-01-01', 'paulo.diretor@escola.edu.br');

-- 5. TURMAS
INSERT INTO turma (serie, turno, ano_letivo, sala_principal) VALUES
('1º Ano EM', 'Matutino', 2025, 101),
('2º Ano EM', 'Matutino', 2025, 102),
('3º Ano EM', 'Matutino', 2025, 201),
('1º Ano EM', 'Vespertino', 2025, 202),
('2º Ano EM', 'Vespertino', 2025, 301);

-- 6. ALUNOS
INSERT INTO aluno (nome, data_nascimento, telefone, email, cod_turma_atual) VALUES
('Pedro Henrique Silva', '2007-03-15', '(11) 91234-5678', 'pedro.silva@email.com', 1),
('Ana Julia Oliveira', '2007-08-22', '(11) 92345-6789', 'ana.oliveira@email.com', 1),
('Lucas Santos Costa', '2006-05-10', '(11) 93456-7890', 'lucas.costa@email.com', 2),
('Beatriz Lima Ferreira', '2006-12-03', '(11) 94567-8901', 'beatriz.ferreira@email.com', 2),
('Gabriel Souza Alves', '2005-09-18', '(11) 95678-9012', 'gabriel.alves@email.com', 3),
('Sophia Pereira Rocha', '2005-11-25', '(11) 96789-0123', 'sophia.rocha@email.com', 3),
('Matheus Santos Lima', '2007-01-07', '(11) 97890-1234', 'matheus.lima@email.com', 4),
('Isabella Costa Silva', '2006-07-14', '(11) 98901-2345', 'isabella.silva@email.com', 5);

-- 7. RELACIONAMENTOS DE PARENTESCO
INSERT INTO parentesco (matricula_aluno, cpf_responsavel, tipo_parentesco) VALUES
(1, '12345678901', 'Mãe'),
(2, '23456789012', 'Pai'),
(3, '34567890123', 'Mãe'),
(4, '45678901234', 'Pai'),
(5, '56789012345', 'Mãe'),
(6, '56789012345', 'Mãe'),
(7, '12345678901', 'Tia'),
(8, '34567890123', 'Avó');

-- 8. AULAS (Grade Horária)
INSERT INTO aula (cod_disciplina, cod_turma, cpf_professor, horario) VALUES
-- TURMA 1
(1, 1, '11111111111', '2.0730-2;4.1010-1'),    -- Segunda 7:30 2 aulas, Quarta 10:10 1 aula
(2, 1, '22222222222', '2.0930-1;4.1110-2'),    -- Segunda 9:30 1 aula, Quarta 11:10 2 aulas
(3, 1, '33333333333', '3.0730-2'),             -- Terça 7:30 2 aulas
(4, 1, '44444444444', '5.1010-3'),             -- Quinta 10:10 3 aulas
(5, 1, '55555555555', '6.0730-2;2.1110-1'),    -- Sexta 7:30 2 aulas, Segunda 11:10 1 aula

-- TURMA 2
(1, 2, '11111111111', '2.0730-2;4.1010-1'),    -- Segunda 7:30 2 aulas, Quarta 10:10 1 aula
(2, 2, '22222222222', '2.0930-1;4.1110-2'),    -- Segunda 9:30 1 aula, Quarta 11:10 2 aulas
(3, 2, '33333333333', '4.1220-2'),             -- Quarta 12:20 2 aulas
(4, 2, '44444444444', '3.0930-2;5.0730-1'),    -- Terça 9:30 2 aulas, Quinta 7:30 1 aula
(5, 2, '55555555555', '6.0730-2;2.1110-1');    -- Sexta 7:30 2 aulas, Segunda 11:10 1 aula

-- 9. CONSELHOS DE CLASSE
INSERT INTO conselho_classe (cod_turma, data_reuniao, cpf_professor, ata_da_reuniao) VALUES
(1, '2024-03-15', '11111111111', 'Reunião do 1º bimestre. Discussão sobre desempenho geral da turma. Alunos apresentaram bom rendimento em matemática. Necessidade de reforço em algumas disciplinas.'),
(2, '2024-03-15', '22222222222', 'Conselho do 1º bimestre - 2º ano. Turma demonstra maturidade e responsabilidade. Alguns alunos precisam melhorar a participação oral.'),
(3, '2024-03-16', '33333333333', 'Reunião preparatória para o ENEM. Discussão sobre cronograma de revisão e simulados. Orientações sobre redação e áreas de conhecimento.');

-- 10. MENSALIDADES
INSERT INTO mensalidade (matricula_aluno, mes_referencia, ano_referencia, valor_base, valor_desconto, data_vencimento, data_pagamento) VALUES
-- Mensalidades pagas
(1, 1, 2024, 800.00, 0.00, '2024-01-10', '2024-01-08'),
(1, 2, 2024, 800.00, 0.00, '2024-02-10', '2024-02-09'),
(1, 3, 2024, 800.00, 80.00, '2024-03-10', '2024-03-05'), -- com desconto

(2, 1, 2024, 800.00, 0.00, '2024-01-10', '2024-01-10'),
(2, 2, 2024, 800.00, 0.00, '2024-02-10', '2024-02-12'),
(2, 3, 2024, 800.00, 0.00, '2024-03-10', NULL), -- em aberto

(3, 1, 2024, 850.00, 0.00, '2024-01-10', '2024-01-07'),
(3, 2, 2024, 850.00, 0.00, '2024-02-10', '2024-02-08'),
(3, 3, 2024, 850.00, 0.00, '2024-03-10', '2024-03-09'),

-- Algumas mensalidades em aberto para demonstrar o sistema
(4, 2, 2024, 850.00, 0.00, '2024-02-10', NULL),
(4, 3, 2024, 850.00, 0.00, '2024-03-10', NULL),

(5, 1, 2024, 900.00, 0.00, '2024-01-10', '2024-01-09'),
(5, 2, 2024, 900.00, 90.00, '2024-02-10', '2024-02-08'), -- com desconto
(5, 3, 2024, 900.00, 0.00, '2024-03-10', NULL);

-- ==============================================================================
-- CONSULTAS DE VERIFICAÇÃO
-- ==============================================================================

SELECT * FROM aluno;
SELECT * FROM turma;
SELECT * FROM aula;
SELECT * FROM disciplina;
SELECT * FROM responsavel;
SELECT * FROM funcionario;
SELECT * FROM sala;
SELECT * FROM professor;
SELECT * FROM parentesco;
SELECT * FROM conselho_classe;
SELECT * FROM mensalidade;