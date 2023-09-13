from autor import Autor
from biblioteca import Biblioteca
from capitulo import Capitulo
from editora import Editora
from livro import Livro

sistema = Biblioteca()
melhoramentos = Editora(8080, "Editora Melhoramens")
vihtube = Autor(7070, "Vih Tube")
zefelipe = Autor(5050, "Ze Felipe")
livrovihtube = Livro(1212, "Aventuras de Vih Tube", 2017, melhoramentos, vihtube, 1, "meu dia ruim")

livrovihtube.incluirAutor(zefelipe)
print(livrovihtube.autor)