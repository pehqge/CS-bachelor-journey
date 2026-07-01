.data

	recebeN: .asciiz "Insira o valor de n: "
	valorResultado: .asciiz "O fatorial de n é: "
	resultado: .word 0

.text

	la $s1, resultado

# ========== INPUT =============

	# ---- imprime no console a frase de entrada ----
	li	$v0, 4
	la	$a0, recebeN
	syscall
	
	# ---- recebe N e coloca em $a0 -----
	li	$v0, 5
	syscall
	move	$a0, $v0	# armazena em $a0 pois é o parametro de entrada de fatorial
	
# ========== FATORIAL ===========

	jal 	fatorial	# calcula fatorial e armazena em $v0
	move	$s0, $v0	# move o resultado para $s0
	sw	$s0, 0($s1)	#armazena o resultado na memória
# ========== OUTPUT =============
	
	# ---- imprime no console a frase de saída ----
	li	$v0, 4
	la	$a0, valorResultado
	syscall
	
	# ---- imprime resultado ----
	move	$a0, $s0
 	li 	$v0, 1
 	syscall
 	 
 	# ---- encerra programa -----
 	li $v0, 10
 	syscall





# ============ FUNÇÃO FATORIAL ============
# recebe  $a0 (N)
# retorna $v0 (N!)

fatorial:
	addi	$sp, $sp, -8 		# incrementa a pilha para armazenar RA e valor
	sw	$ra, 0($sp)		# salva o ra atual no 1o slot
	sw	$s0, 4($sp)		# salva o n atual no 2o slot
	
	li	$v0, 1			# retorna 1
	beq	$a0, $zero, return	# se caso, n chegar em 0, a funcao acaba
	
	add	$s0, $a0, $zero
	addi	$a0, $a0, -1		# subtrai 1 de n
	jal 	fatorial
	
	mul	$v0, $s0, $v0		# multiplicação recursiva
	
	return:	
		lw 	$ra, 0($sp)	#recupera o endereço de retorno na pilha
		lw	$s0, 4($sp)	#recpera o endereço de n-1 na pilha
		addi	$sp, $sp, 8	#limpa a pilha
		jr	$ra		#volta para o último endereço recuperado
