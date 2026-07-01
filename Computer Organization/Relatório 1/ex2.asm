# Programa para calcular:
# a = b + 35
# c = d - a + e

.data # Armazenando as variaveis na memoria de dados

	A: .word 0 # iniciada com 0 pois sera atribuido o resultado posteriormente
	B: .word 0
	C: .word 0
	D: .word 20
	E: .word 25
	
	# strings para imprimir no console
	valorA: .asciiz "Valor de A após operação (A = B + 35): "
	newline: .asciiz "\n"
	valorC: .asciiz "Valor de C após operação (C = D - A + E): "
	recebeInput: .asciiz "Escreva o valor inteiro de B: "

.text
	# ---- alocando variaveis no registrador (carregando os endereços)----
	la	$s0, A  
	la	$s1, B
	la	$s2, C
	la	$s3, D
	la	$s4, E
	
	# ---- recebendo B por teclado -----
	
	# imprimindo mensagem para receber o valor de B
	li	$v0, 4
	la	$a0, recebeInput
	syscall
	
	# recebendo a entrada (input)
	li 	$v0, 5 # carrega comando para ler um inteiro
	syscall 
	move 	$t1, $v0 # salva o inteiro fornecido pelo teclado para o registrador t0
	sw	$t1, 0($s1) # salvando B na memoria de dados
	
	# imprime nova linha em branco
	li	$v0, 4
	la	$a0, newline
	syscall
	
	# ---- 1a operacao A = B + 35 -----
	addi	$t0, $t1, 35 # salvando B + 35 no registrador temporário 
	sw	$t0, 0($s0) # carregando conteúdo do temporário no registrador destino na memória
	
	# ----- imprimindo resultado de A -----
	
	# imprimindo string para indicar o resultado obtido para 'A'
	li	$v0, 4
	la	$a0, valorA
	syscall
	
	# imprimindo o resultado de A
	li	$v0, 1
	li	$a0, 0
	add	$a0, $a0, $t0
	syscall
	
	# imprimindo nova linha
	li	$v0, 4
	la	$a0, newline
	syscall
	
	# ---- 2a operacao C = D - A + E -----
	
	lw	$t3, 0($s3) # carregando D
	lw	$t4, 0($s4) # carregando E
	
	sub	$t2, $t3, $t0 # carregando D - A em temp C
	add	$t2, $t2, $t4 # carregando resultado anterior + E em temp C
	
	sw	$t2, 0($s2) # salvando o resultado em C
	
	# ----- imprimindo resultado de C -----
	
	# imprimindo string  para indicar o resultado obtido para 'C'
	li	$v0, 4
	la	$a0, valorC
	syscall
	
	# imprimindo o resultado de C
	li	$v0, 1
	li	$a0, 0 # limpando a0
	add	$a0, $a0, $t2
	syscall