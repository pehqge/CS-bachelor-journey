.data
	vetorA: .space 4000	#aloca 1000 espaços no array
 	vetorB: .space 4000	#aloca 1000 espaços no array

	# ---- strings para imprimir no console ----
	recebeN: .asciiz "Insira o tamanho N dos vetores: "
	recebeA: .asciiz "\nInsira os valores do vetor A abaixo:\n"
	recebeB: .asciiz "\nInsira os valores do vetor B abaixo:\n"
	mediaA:	.asciiz "\nMedia de A: "
	mediaB:	.asciiz "\nMedia de B: "
	
.text
	######### Alocando vetores #########

	la	$s0, vetorA			# endereço base do vetor A
	la 	$s1, vetorB			# endereço base do vetor B
	
	######### Recebendo N e Vetores do console #########
	
	# ---- imprime mensagem para receber n ----
	li 	$v0, 4
	la 	$a0, recebeN
	syscall
	
	# ---- recebe n ----	
	li 	$v0, 5
	syscall
	move 	$t0, $v0			# n fica armazenado em $t0

	# ---- imprime mensagem para receber vetor A ----	
	li 	$v0, 4
	la 	$a0, recebeA
	syscall

	# ---- recebe vetor A e preenche com os valores recebido do teclado ----
	li 	$t2, 0
	addi 	$t4, $s0, 0			# copia o endereço base para t4, assim não perdemos ele

	preenche_A:	
		li 	$v0, 6			# comando p receber float
		syscall
		s.s 	$f0,  0($t4)		# carrega o float lido na posição do vetor
		addi 	$t4, $t4, 4		# pega a próxima posição do vetor
		addi 	$t2, $t2, 1		# incrementa registrador auxiliar
		bne 	$t0, $t2, preenche_A	# repete o loop enquanto os N valores não forem lidos
		
	# ---- imprime mensagem para receber vetor B ----	
	li 	$v0, 4
	la 	$a0, recebeB
	syscall

	# ---- recebe vetor B e preenche com os valores recebido do teclado----
	li 	$t2, 0
	addi 	$t3, $s1, 0			# copia o endereço base para t3, assim não perdemos ele

	preenche_B:	
		li 	$v0, 6			# comando p receber float
		syscall
		s.s	$f0,  0($t3)		# carrega o float lido na posição do vetor
		addi 	$t3, $t3, 4		# pega a próxima posição do vetor
		addi 	$t2, $t2, 1		# incrementa registrador auxiliar
		bne 	$t0, $t2, preenche_B	# repete o loop enquanto os N valores não forem lidos

	######### Calculando Média #########
	
	move 	$a0, $s0			# salva o endereço base em a0 para passar como argumento do procedimento
	move 	$a1, $s1			# salva o endereço base em a1 para passar como argumento do procedimento
	jal 	media				# resultados em $f2 (vetor A) e $f4 (vetor B)
	
	######### Imprimindo resultados no Console #########
	
	# ---- imprime mensagem para resultado do vetor A  ----	
	li 	$v0, 4
	la 	$a0, mediaA
	syscall
	# ---- imprime resultado do vetor A  ----	
	li 	$v0, 2
	mov.s	$f12, $f2
	syscall

	# ---- imprime mensagem para resultado do vetor B  ----	
	li 	$v0, 4
	la 	$a0, mediaB
	syscall
	# ---- imprime resultado do vetor B  ----	
	li 	$v0, 2
	mov.s	$f12, $f4
	syscall
	
	# ---- encerra programa ----
	li 	$v0, 10
	syscall
	
	
	########################### procedimento média #############################
	
	
media:
	li 	$t2, 0				# registrador para controlar o loop
	
	loop_soma:
		l.s 	$f14, 0($a0)
		l.s 	$f16, 0($a1)
		add.s 	$f2, $f2, $f14		# somaA += vetA[i]
		add.s 	$f4, $f4, $f16		# somaB += vetB[i]
		addi 	$a0, $a0, 4		# pega a proxima posição do vetor A
		addi 	$a1, $a1, 4		# pega a proxima posição do vetor B
		addi 	$t2, $t2, 1
		bne 	$t0, $t2, loop_soma	# repete o loop enquanto a soma de todos os valores dos vetores não for finalizada
		
		
	mtc1 	$t0, $f6			# move o valor de N para f6
	cvt.s.w $f6, $f6			# converte para precisão simples, para efetuar a divisão
	div.s 	$f2, $f2, $f6			# divide a soma do vetor A pelos N elementos
	div.s 	$f4, $f4, $f6			# divide a soma do vetor B pelos N elementos
		
	jr 	$ra
