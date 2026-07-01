.data
	A:		.word	4
	B:		.word	5
	RESULTADO: 	.word 	0	#armazena o resultado
.text
j main

multiplicacao:
	li 	$t2, 0   # inicia contador em 0
	li	$t3, 0  # inicia soma acumulada em 0

	loop_mult:
		add	$t3, $t3, $a0  # soma da mult
		addi	$t2, $t2, 1    # incrementa contador
		
		bne	$a1, $t2, loop_mult  # se ainda n�o acabou a mult, volta para somar de novo
	
	addi	$v0, $t3, 0 # armazena o resultado da multiplica��o
	jr 	$ra #volta para o chamados
	

main:
	# ----- salvando dados da mem�ria -----
	
	la	$s0, A	#salvando endere�o de A
	la	$s1, B	#salvando endere�o de B
	la	$s3, RESULTADO	#salvando endere�o de resultado
	
	
	lw	$t0, 0($s0) #carrega o conteudo de s0 (A) para t0
	lw	$t1, 0($s1)#carrega o conteudo de s1 (B) para t1
	
	# ----- armazenando os argumentos da fun��o em a0 e a1 -----
	
	addi	$a0, $t0, 0 #armazena A
	addi	$a1, $t1, 0#armazena B
	
	# ----- chamando a funcao -----
	jal	multiplicacao #chama a fun��o multiplica��o

	sw	$v0, 0($s3) #salvando o resultado na mem�ria