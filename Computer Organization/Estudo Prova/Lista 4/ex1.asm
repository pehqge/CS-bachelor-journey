.text
	j main
	
calcula:
	add	$t0, $s0, $s1
	add	$t1, $s2, $s3
	sub	$t0, $t0, $t1
	
	add	$v0, $t0, $zero
	jr	$ra

main:
	li	$v0, 5
	syscall
	move	$s0, $v0
	
	li	$v0, 5
	syscall
	move	$s1, $v0
	
	li	$v0, 5
	syscall
	move	$s2, $v0
	
	li	$v0, 5
	syscall
	move	$s3, $v0
	
	jal calcula
	move	$s4, $v0