from biblioteca import *


# iniciando livros (1. cadastre 4 livros)
livro_kefera = Livro("Mais que cinco minutos", "um grande livro de uma grande youtuber",
                     "Kefera Bukman", "kefera", "auto-biografia", "livre")
livro_tudosobre = Livro("Tudo sobre o autoritarismo brasileiro",
                        "Um resumo sobre o histórico do autoritarismo na sociedade brasileira", "Lilia Schwarcz", "Não tem", "sociologia", "14+")
livro_galinhapintadinha = Livro("Galinha Pintadinha para menores", "Se divirta com a turminha da nossa querida galinha",
                                "Pintadinha, Galinha", "Galinha Pintadinha", "infatil", "livre")
livro_biblia = Livro("Biblia", "O maior best seller mundial",
                     "Muitos", "Jesus Cristo", "Religioso", "Livre")

# iniciando amigos (2. cadastre 3 amigos)
rodrigo = Amigo("Rodrigo", ["(11) 99847-7878"], "rodrigo@gmail.com")
pablo = Amigo("Pablo", ["+1 (356) 3987-843"], "pablopascal@gmail.com")
tommy = Amigo("Tommy", ["(21) 99876-0998"], "tommy@gmail.com")

# iniciando sistema
biblioteca = BibliotecaPessoal(
    [rodrigo, pablo], [livro_kefera, livro_tudosobre, livro_galinhapintadinha])

# teste de adição
biblioteca.adiciona_amigo(tommy)
biblioteca.adiciona_livro(livro_biblia)

# confirmando se as adições deram certo
print("Amigos registados:")
print(", ".join([x.nome for x in biblioteca.amigos]))
print("Livros registados:")
print(", ".join([x.titulo for x in biblioteca.livros]))
print()

# 3. registre o emprestimo de um livro ao 1o amigo
biblioteca.empresta_livro(rodrigo, livro_kefera,
                          datetime.today)

# 4. mostre os livros emprestados
print("Livros emprestados")
print("\n".join(str(x) for x in biblioteca.ver_livros_emprestados()))
print()

# 5. registre 2 emprestimos ao segundo amigo
biblioteca.empresta_livro(tommy, livro_galinhapintadinha, datetime.today)
biblioteca.empresta_livro(tommy, livro_biblia, datetime.today)

# 6. mostre os livros emprestados
print("Livros emprestados")
print("\n".join(str(x) for x in biblioteca.ver_livros_emprestados()))
print()

# 7. registre a devolucao do livro do primeiro emprestimo
biblioteca.devolve_livro(livro_kefera, datetime.today)

# 8. mostre os livros emprestados
print("Livros emprestados")
print("\n".join(str(x) for x in biblioteca.ver_livros_emprestados()))
