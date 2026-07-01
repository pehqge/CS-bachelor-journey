.data
	sinal:	.double -1
	um:	.double 1
	input:	.asciiz "Digite o número para calcular o seno (em radianos): "
	output:	.asciiz "O valor aproximado do seno é: "
	
.text

	j	main
	
# ===== FUNÇÃO FATORIAL ======
# calcula n!
# parametro: n ($a0)
# saída: n! ($f4)


fatorial:
	addi	$sp, $sp, -8 		# incrementa a pilha para armazenar RA e valor
	sw	$ra, 0($sp)		# salva o ra atual no 1o slot
	sw	$s0, 4($sp)		# salva o n atual no 2o slot
	
	l.d	$f4, um			# retorna 1
	beq	$a0, $zero, acaba	# se caso, n chegar em 0, a funcao acaba
	
	move	$s0, $a0
	addi	$a0, $a0, -1		# subtrai 1 de n
	jal 	fatorial
	
	mtc1	$s0, $f14		# conversao para double para suportar numeros grandes
	cvt.d.w	$f14, $f14
	
	mul.d	$f4, $f14, $f4		# salva saida em f4
	
	acaba:	
		lw 	$ra, 0($sp)
		lw	$s0, 4($sp)
		addi	$sp, $sp, 8
		jr	$ra
	
# ====== FUNÇÃO POTENCIAÇÃO ======
# calcula x**n
# parametros: x ($f2) e n ($a0)
# saída: x**n ($f8)

potencia:
# ----- Salva 1 como double -----
	l.d	$f8, um
	
# ----- Se n = 0, retorna 1 ------
	beq	$a0, 0, exit_potencia
	
# ---- Faz loop até chegar em x**n -----
	li	$t0, 0
	
	loop:
		mul.d	$f8, $f8, $f2	# valor *= x
		addi	$t0, $t0, 1
		bne	$t0, $a0, loop	# faz o loop enquanto não chegar em n

	exit_potencia:
	jr	$ra
	
# ====== FUNÇÃO SENO ======
# calcula seno pela somatória (((-1)**n) / (2*n + 1)! ) *  x**(2*n + 1) em que n está em [0, 20]
# parametro: x ($f0)
# saída: seno ($f12)

seno:
	move	$s1, $ra	# salva o ra em s1

# ------ Inicia seno em 0 -----
	li 	$t0, 0
	mtc1	$t0, $f12
	cvt.d.w	$f12, $f12
	
# ------ Realiza as 20 iterações da somatória -----
	li	$t1, 0		# n da somatoria
	
loop_soma:
	
	# ----- calcula o sinal ------
	
	l.d	$f2, sinal	# $f2 = -1
	move	$a0, $t1	# $a0 = n
	
	jal	potencia	# sinal está salvo em $f8
	
	# ----- calculando fat = 2*n + 1 -------
	
	add	$t2, $t1, $t1	# fat = n+n
	addi	$t2, $t2, 1	# fat += 1
	
	# ----- calculando fator = sinal / (fat)! -------
	
	move	$a0, $t2 	# iniciando parametro pra funcao fatorial
	
	jal	fatorial
	
	div.d	$f4, $f8, $f4	# fator = sinal / (fat)!
	
	# ----- calculando x2 = x ** fat ------
	
	# iniciando parametros da potenciacao
	mov.d	$f2, $f0
	move	$a0, $t2
	
	jal	potencia
	
	# ----- calculando fator * x2 ------
	mul.d	$f6, $f4, $f8	# interno = fator * x2
	add.d	$f12, $f12, $f6	# seno += interno
	
	# ----- volta pro loop se n < 20 ------
	addi	$t1, $t1, 1
	bne	$t1, 20, loop_soma
	
	move	$ra, $s1	# restaura ra
	jr	$ra
	
# ======== MAIN ===========

main:
# ----- Leitura de dados ------

	# imprime "Digite o numero..." no console
	
	la	$a0, input	# recebe a frase
	li	$v0, 4		# código impressão no console
	syscall
	
	# recebe o double
	
	li	$v0, 7		# código leitura de double
	syscall 		# o número digitado está em $f0
	
# ------ Chamando a função ------

	jal seno
	
# ------ Imprimindo resultado ------

	# imprime "O valor aproximado..." no console
	
	la	$a0, output	# recebe a frase
	li	$v0, 4		# código impressão no console
	syscall
	
	# imprime o valor calculado
	
	li	$v0, 3		# código impressão de double
	syscall 		# o resultado já está no $f12
	
# ----- Encerra programa ------
	
	li	$v0, 10
	syscall
