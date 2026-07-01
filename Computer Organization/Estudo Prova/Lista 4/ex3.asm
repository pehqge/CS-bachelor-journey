.data
	impPow: .asciiz 	"A potencia resultante é: "
	inputB: .asciiz		"Escreva uma base: "
	inputE: .asciiz	 	"Escreva um expoente: "
	nl:	.asciiz 	"\n"
	
.text
	j	main

pow:
	li	$t0, 1
	
	li	$t1, 0
	pow_for:
	mul	$t0, $t0, $a0
	addi	$t1, $t1, 1
	blt	$t1, $a1, pow_for
	
	move 	$v0, $t0
	
	jr	$ra


main:
	li	$v0, 4
	la	$a0, inputB
	syscall
	
	li	$v0, 5
	syscall
	move	$s0, $v0
	
	li	$v0, 4
	la	$a0, nl
	syscall
	
	
	li	$v0, 4
	la	$a0, inputE
	syscall
	
	li	$v0, 5
	syscall
	move	$s1, $v0
	
	li	$v0, 4
	la	$a0, nl
	syscall
	
	move	$a0, $s0
	move	$a1, $s1
	
	jal	pow
	
	move	$s3, $v0
	