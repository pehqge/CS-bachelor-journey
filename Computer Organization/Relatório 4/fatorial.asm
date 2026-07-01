########precisa ser adaptada para o código do ex2


.data
	numero: .word 5
	

.text

main:
	la $s0, numero
	lw $a0, 0($s0)
	
	jal fatorial
	
	move $s1, $v0


fatorial:
	addi $sp,$sp, -8		#espaço para  na pilha
	sw $ra, 4($sp)			#salva o endereço de retorno na pilha no fundo da pilha
	sw $a0, 0($sp)			#salva o argumento (n)
	
	slti $t0, $a0,1			#testa se n<1. Se verdadeito %t0 = 1, se não $t0=0. Inicialmente vai ser falso, ent�o executa li
	beq $t0, $zero, subtrai
	
	li $v0, 1			#se for, devolve 1
	add $sp, $sp, 8			#limpa a pilha
	jr $ra				#vai para a linha 30 e começa a multiplicação com os 'n-1' armazenados enquanto limpa a pilha
	
subtrai:
	sub $a0, $a0, 1			#atualiza o argumento para n-1
	jal fatorial			#chama fatorial para n-1
		
	lw $a0, 0($sp)			#recupera o argumento
	lw $ra, 4($sp)			#recupera o endereço de retorno
	add $sp, $sp, 8			#limpa a pilha
	
	mul $v0, $a0, $v0		#calcula n*fatorial(n-1)
	jr $ra				#volta para o ultimo endereço da pilha (linha 30, até chegar no endereço da main)
