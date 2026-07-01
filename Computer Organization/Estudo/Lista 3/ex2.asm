# calcular somatoria 1 a 5
.text
	li	$t0, 1			# t0 = i
somatorio:	
	add	$t1, $t1, $t0		# t1 = t1 + i
	addi	$t0, $t0, 1			# i += 1
	
	li	$t2, 6
	bne	$t0, $t2, somatorio
	add	$s0, $zero, $t1
	