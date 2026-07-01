.data
	input: .asciiz	"\nDigite um numero para achar seu fatorial: "
	output:	.asciiz	"\nO fatorial resultou em: "

.text
j main

fatorial:
	addi	$sp, $sp, -8
	sw	$ra, 0($sp)
	sw	$s0, 4($sp)
	
	li	$v0, 1
	beq	$a0, $zero, fim
	
	move	$s0, $a0
	addi	$a0, $a0, -1
	
	jal 	fatorial
	mul	$v0, $v0, $s0
	
fim:
	lw	$ra, 0($sp)
	lw	$s0, 4($sp)
	addi	$sp, $sp, 8
	
	jr	$ra
	
	
main:
	li	$v0, 4
	la	$a0, input
	syscall
	
	li	$v0, 5
	syscall
	move	$a0, $v0
	

	jal 	fatorial
	move	$s2, $v0
	
	li	$v0, 4
	la	$t0, output
	move	$a0, $t0
	syscall
	
	li	$v0, 4
	li	$a0, 0
	add	$a0, $a0, $s2
	syscall