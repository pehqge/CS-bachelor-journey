li $v0, 5 # salva a constante 5 (ler inteiro) em v0 (variavel de comando)
syscall # sistema faz o comando
move $t0, $v0 # salva o inteiro dado para t0

li $v0, 1 # Sobrescreve 1 (print) em v0 
addi $a0, $a0, 12 # Adiciona 12 a a0 (variavel de saida para console)
syscall # printa

