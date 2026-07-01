/*
    Script de criação do schema do Banco de Dados Escolar
    Disciplina: Banco de Dados I
    Grupo: Breno da Silva Pereira, Caio César Aquino, João Vitor Curcio Sutter,
    João Pedro Tamburo Faraoni, Pedro Henrique Gimenez
*/

-- ==============================================================================
-- 1. TABELAS INDEPENDENTES (ENTIDADES FORTES)
-- ==============================================================================

-- Tabela: SALA
-- Armazena as informações físicas das salas de aula.
CREATE TABLE sala (
    numero INT PRIMARY KEY,
    andar INT NOT NULL,
    capacidade INT NOT NULL,

    -- Garante que a capacidade seja um valor lógico positivo
    CONSTRAINT ck_sala_capacidade CHECK (capacidade > 0)
);

-- Tabela: DISCIPLINA
-- Catálogo das disciplinas ofertadas pela escola.
CREATE TABLE disciplina (
    codigo SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE, -- Nomes únicos para evitar duplicidade
    carga_horaria INT NOT NULL,
    ementa TEXT,

    CONSTRAINT ck_disciplina_carga CHECK (carga_horaria > 0)
);

-- Tabela: FUNCIONARIO
-- Registro geral de todos os colaboradores da escola.
CREATE TABLE funcionario (
    cpf CHAR(11) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    salario DECIMAL(10, 2) NOT NULL,
    funcao VARCHAR(50) NOT NULL,
    data_admissao DATE NOT NULL DEFAULT CURRENT_DATE,
    email_corporativo VARCHAR(100) UNIQUE,
    
    CONSTRAINT ck_funcionario_salario CHECK (salario > 0),
    -- Padronização dos cargos aceitos no sistema
    CONSTRAINT ck_funcionario_funcao CHECK (funcao IN ('Professor', 'Coordenador', 'Diretor', 'Administrativo', 'Zeladoria'))
);

-- Tabela: RESPONSAVEL
-- Dados dos pais ou tutores legais dos alunos.
CREATE TABLE responsavel (
    cpf CHAR(11) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    email VARCHAR(100) NOT NULL,
    endereco VARCHAR(200) NOT NULL
);

-- ==============================================================================
-- 2. TABELAS DEPENDENTES - NÍVEL 1
-- ==============================================================================

-- Tabela: PROFESSOR
-- Especialização da tabela funcionário (relação 1:1).
CREATE TABLE professor (
    cpf CHAR(11) PRIMARY KEY,

    -- Chave estrangeira que também é primária (Herança)
    -- Se o funcionário for removido, o professor também será.
    CONSTRAINT fk_professor_funcionario FOREIGN KEY (cpf) 
        REFERENCES funcionario(cpf) ON DELETE CASCADE
);

-- Gatilho para inserir professor automaticamente ao cadastrar um funcionário com função 'Professor'
CREATE OR REPLACE FUNCTION trg_auto_criar_professor()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.funcao = 'Professor' THEN
        INSERT INTO professor (cpf) VALUES (NEW.cpf);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tg_cria_professor_automaticamente
AFTER INSERT ON funcionario
FOR EACH ROW
EXECUTE FUNCTION trg_auto_criar_professor();

-- Tabela: TURMA
-- Grupos de alunos organizados por série e ano letivo.
CREATE TABLE turma (
    codigo SERIAL PRIMARY KEY,
    serie VARCHAR(20) NOT NULL,
    turno VARCHAR(20) NOT NULL,
    ano_letivo SMALLINT NOT NULL,
    sala_principal INT NOT NULL,
    
    CONSTRAINT fk_turma_sala FOREIGN KEY (sala_principal) 
        REFERENCES sala(numero),
        
    CONSTRAINT ck_turma_turno CHECK (turno IN ('Matutino', 'Vespertino', 'Noturno', 'Integral')),
    CONSTRAINT ck_turma_ano CHECK (ano_letivo >= 1900)
);

-- ==============================================================================
-- 3. TABELAS DEPENDENTES - NÍVEL 2
-- ==============================================================================

-- Tabela: ALUNO
-- Dados cadastrais dos discentes.
CREATE TABLE aluno (
    matricula SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    data_nascimento DATE NOT NULL,
    telefone VARCHAR(20),
    email VARCHAR(100),
    cod_turma_atual INT,
    
    CONSTRAINT fk_aluno_turma FOREIGN KEY (cod_turma_atual) 
        REFERENCES turma(codigo),
        
    -- Validação simples para evitar datas futuras
    CONSTRAINT ck_aluno_nascimento CHECK (data_nascimento <= CURRENT_DATE)
);

-- Tabela: AULA (Associativa)
-- Representa a grade horária: Disciplina X Turma X Professor.
CREATE TABLE aula (
    cod_disciplina INT NOT NULL,
    cod_turma INT NOT NULL,
    cpf_professor CHAR(11) NOT NULL,
    horario VARCHAR(50) NOT NULL, -- Ex: "2.0730-3"
    
    -- Chave Primária Composta: Uma disciplina só ocorre uma vez por turma
    PRIMARY KEY (cod_disciplina, cod_turma),
    
    CONSTRAINT fk_aula_disciplina FOREIGN KEY (cod_disciplina) 
        REFERENCES disciplina(codigo),
    CONSTRAINT fk_aula_turma FOREIGN KEY (cod_turma) 
        REFERENCES turma(codigo),
    CONSTRAINT fk_aula_professor FOREIGN KEY (cpf_professor) 
        REFERENCES professor(cpf)
);

-- Tabela: CONSELHO_CLASSE
-- Registro das reuniões pedagógicas por turma.
CREATE TABLE conselho_classe (
    codigo SERIAL PRIMARY KEY,
    cod_turma INT NOT NULL,
    data_reuniao DATE NOT NULL,
    cpf_professor CHAR(11) NOT NULL, -- Professor responsável pela ata
    ata_da_reuniao TEXT NOT NULL,
    
    CONSTRAINT fk_conselho_turma FOREIGN KEY (cod_turma) 
        REFERENCES turma(codigo) ON DELETE CASCADE,
    CONSTRAINT fk_conselho_professor FOREIGN KEY (cpf_professor) 
        REFERENCES professor(cpf)
);

-- ==============================================================================
-- 5. TABELAS DEPENDENTES - NÍVEL 3
-- ==============================================================================

-- Tabela: PARENTESCO (Associativa)
-- Relaciona Alunos e Responsáveis (N:N).
CREATE TABLE parentesco (
    matricula_aluno INT NOT NULL,
    cpf_responsavel CHAR(11) NOT NULL,
    tipo_parentesco VARCHAR(20) NOT NULL, -- Pai, Mãe, Tutor, Avô, etc.
    
    PRIMARY KEY (matricula_aluno, cpf_responsavel),
    
    CONSTRAINT fk_parentesco_aluno FOREIGN KEY (matricula_aluno) 
        REFERENCES aluno(matricula) ON DELETE CASCADE,
    CONSTRAINT fk_parentesco_responsavel FOREIGN KEY (cpf_responsavel) 
        REFERENCES responsavel(cpf) ON DELETE CASCADE
);

-- Gatilho para deletar responsável automaticamente quando não houver mais alunos vinculados
CREATE OR REPLACE FUNCTION trg_deletar_responsavel_sem_alunos()
RETURNS TRIGGER AS $$
BEGIN
    -- Verifica se o responsável ainda tem outros parentescos
    IF NOT EXISTS (
        SELECT 1 FROM parentesco 
        WHERE cpf_responsavel = OLD.cpf_responsavel
    ) THEN
        -- Se não tiver mais nenhum parentesco, deleta o responsável
        DELETE FROM responsavel WHERE cpf = OLD.cpf_responsavel;
    END IF;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tg_deletar_responsavel_sem_alunos
AFTER DELETE ON parentesco
FOR EACH ROW
EXECUTE FUNCTION trg_deletar_responsavel_sem_alunos();

-- Tabela: MENSALIDADE
-- Controle financeiro dos alunos.
CREATE TABLE mensalidade (
    codigo SERIAL PRIMARY KEY,
    matricula_aluno INT NOT NULL,
    mes_referencia SMALLINT NOT NULL,
    ano_referencia SMALLINT NOT NULL,
    valor_base DECIMAL(10, 2) NOT NULL,
    valor_desconto DECIMAL(10, 2) DEFAULT 0,
    data_vencimento DATE NOT NULL,
    data_pagamento DATE, -- Pode ser nulo (em aberto)
    
    CONSTRAINT fk_mensalidade_aluno FOREIGN KEY (matricula_aluno) 
        REFERENCES aluno(matricula) ON DELETE CASCADE,
        
    CONSTRAINT ck_mensalidade_mes CHECK (mes_referencia BETWEEN 1 AND 12),
    CONSTRAINT ck_mensalidade_valor CHECK (valor_base >= 0)
);

-- Gatilho para permitir deleção de aluno apenas se todas as mensalidades foram pagas
CREATE OR REPLACE FUNCTION trg_verificar_mensalidades_antes_deletar_aluno()
RETURNS TRIGGER AS $$
DECLARE
    mensalidades_nao_pagas INT;
BEGIN
    -- Conta quantas mensalidades não foram pagas (data_pagamento IS NULL)
    SELECT COUNT(*) INTO mensalidades_nao_pagas
    FROM mensalidade
    WHERE matricula_aluno = OLD.matricula
      AND data_pagamento IS NULL;
    
    -- Se houver mensalidades não pagas, bloqueia a deleção
    IF mensalidades_nao_pagas > 0 THEN
        RAISE EXCEPTION 'Não é possível deletar aluno com mensalidades em aberto. Total de mensalidades não pagas: %', mensalidades_nao_pagas;
    END IF;
    
    -- Se todas foram pagas, permite a deleção (as mensalidades serão deletadas em cascata)
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tg_verificar_mensalidades_antes_deletar_aluno
BEFORE DELETE ON aluno
FOR EACH ROW
EXECUTE FUNCTION trg_verificar_mensalidades_antes_deletar_aluno();
