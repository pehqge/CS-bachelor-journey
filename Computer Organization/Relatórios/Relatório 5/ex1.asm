.data

	resultado: .word 0
	n: .word 0

	# ---- strings para imprimir no console ----
	recebeN: .asciiz "Insira o valor de n: "
	newLine: .asciiz "\n"
	valorResultado: .asciiz "O fatorial de n é: "
.text
	la $s0, resultado
	la $s1, n
	
	# ---- recebendo n por teclado -----
 	# ---- imprime mensagem para receber o valor de n ----
 	li $v0, 4
 	la $a0, recebeN
 	syscall
 	
 	# ---- recebe o valor de n ----
 	li $v0, 5	#comando para ler inteiro
 	syscall
 	move $t0, $v0	#salva o inteiro lido em $t0
 	
 fatorial:
 		li $t1, 1 #controla o loop
 		li $t2, 1 #armazena as multiplicações sucessivas
 		
 		
 		loop:
 			
 			mul $t2, $t0, $t2	#(n-1)*n
 			subi $t0, $t0, 1	#n-1
 			bne $t0, $t1, loop	#procura se n = 1
 			
 			sw $t2, 0($s0)
 
 	# ---- imprime nova linha ----	
 	li $v0, 4
 	la $a0, valorResultado
 	syscall
 	
 	 # ---- imprime resultado ----
 	 li $v0, 1
 	 li $a0, 0
 	 add $a0, $a0, $t2
 	 syscall
 	 
 	 
 