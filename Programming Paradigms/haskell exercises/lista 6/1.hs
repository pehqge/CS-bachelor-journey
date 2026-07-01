-- Crie um tipo de dados Aluno, usando type, assim como criamos um tipo de dados Pessoa. O tipo Aluno deve possuir um campo para o nome, outro para a disciplina e outros tres campos para notas. Agora, execute os passos abaixo.

type Nome = String
type Disciplina = String
type Nota = Float

type Aluno = (Nome, Disciplina, Nota, Nota, Nota)

-- Crie uma funcao no mesmo estilo que a funcao pessoa, vista em sala e disponivel nos slides no Moodle, ou seja, que receba um inteiro e retorne um Aluno correspondente ao valor inteiro.

-- Crie alguns alunos de exemplo, assim como tamb´em feito no exemplo da pessoa

aluno :: Int -> Aluno
aluno 1 = ("Joao", "Matematica", 7.0, 8.0, 9.0)
aluno 2 = ("Maria", "Portugues", 6.0, 7.0, 8.0)
aluno 3 = ("Pedro", "Computação", 9.0, 8.5, 10.0)


-- No main, imprima o primeiro nome de um aluno, portanto crie uma funcao para obter o primeiro nome.

getNome :: Aluno -> Nome
getNome (nome, _, _, _, _) = nome

-- Crie uma funcao que receba um Int e retorne a media do aluno correspondente.

getMediaAluno :: Aluno -> Float
getMediaAluno (_, _, nota1, nota2, nota3) = (nota1 + nota2 + nota3) / 3

getMedia :: Int -> Float
getMedia x = getMediaAluno (aluno x)

-- Crie uma funcao que calcule a media da turma, ou seja, considerando todos os alunos.
