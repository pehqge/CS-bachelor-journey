.data

	resultado: .double 0.0
	estimativa: .double 1.0
	x: .double 1.0		#valor inicial de x
	dois: .double 2.0
 	.align 2		#alinhando para inteiro
 	N: .word 0	

	# ---- strings para imprimir no console ----
	recebeN: .asciiz "Insira o valor de N: "
	recebeX: .asciiz "Insira o valor de X: "
	newline: .asciiz "\n"

.text
j main

raiz_quadrada:


	l.d $f4, 0($s2)			#inicia o registrador estimativa com 1.0
	li $t0, 2			#inicia a constante 2
	mtc1 $t0, $f6			#manda para f6
	cvt.d.w $f6,$f6			#converte para double

    loop:   
 	addi $a0, $a0,-1		#decrementa o valor de n (iterações)
	div.d $f2, $f0, $f4 		#registrador auxiliar(f2) = (x/estimativa)
  	add.d $f2,$f2, $f4		#registrador auxiliar(f2) = (x/estimativa) + estimativa
 	div.d $f2, $f2, $f6		#registrador auxiliar(f2) = (x/estimativa) + estimativa/2
 	mov.d $f4, $f2			#atualiza a estimativa
 	bnez $a0, loop		#se n != 0, vai para o loop e repete novamente, caso contr�rio volta para a main

 	jr $ra				#volta para a main
 	
main:
	# ---- alocando variaveis no registrador (carregando os endere?os)----
   	la $s0, x
   	la $s1, resultado 
	la $s2, estimativa
	la $s3, dois

	# ---- recebendo X por teclado -----
 	# ---- imprime mensagem para receber o valor de x ----
   	li $v0, 4
   	la $a0, recebeX
   	syscall

	# ---- recebe a entrada X do teclado ----
   	li $v0, 7		#comando para ler precisao dupla (vai ficar armazenado em $f0)
   	syscall


   
	# ---- imprime nova linha em branco ----
	li	$v0, 4
	la	$a0, newline
	syscall

	# ---- recebendo N por teclado -----

	# ---- imprime mensagem para receber o valor de n -----
   	li $v0, 4
	la $a0, recebeN
 	syscall

	#---- recebe a entrada N do teclado ----
	li $v0, 5		#comando para ler inteiro
 	syscall
	move $a0, $v0		#salva o inteiro N lido no teclado em $t0
  

  	# ---- chama o procedimento -----
 	jal raiz_quadrada
 	s.d $f4 0($s1)		#salva a estimativa na mem�ria
 	# ---- tirando a raiz quadrada com a fun��o sqrt.d para comparar com o resultado do procefumento -----
 	l.d $f10, 0($s3)
 	sqrt.d $f12, $f10	#tirando a raiz quadrada com sqrt.d para comparar com o valor obtido
