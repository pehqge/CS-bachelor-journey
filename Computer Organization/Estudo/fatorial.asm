.data
	A: .word 5			# variavel para calcular fatorial
	
.text
	lw	$a0, A  		# salva o valor de A em a0 para passar como parametro
	jal	fatorial		# vai para fact e armazena o endereço em RA
	j exit
	
	
fatorial:
	addi	$sp, $sp, -8 		# incrementa a pilha para armazenar RA e valor
	sw	$ra, 0($sp)		# salva o ra atual no 1o slot
	sw	$s0, 4($sp)		# salva o n atual no 2o slot
	
	li	$v0, 1			# retorna 1
	beq	$a0, $zero, acaba	# se caso, n chegar em 0, a funcao acaba
	
	add	$s0, $a0, $zero
	addi	$a0, $a0, -1		# subtrai 1 de n
	jal 	fatorial
	
	mul	$v0, $s0, $v0
	
acaba:	
	lw 	$ra, 0($sp)
	lw	$s0, 4($sp)
	addi	$sp, $sp, 8
	jr	$ra
	
exit:
	li	$s1, 2
	lw	$s0, 4($sp)
