.text
	li	$s0, 5
	li	$s1, 7
	
	bgt	$s0, $s1, a
	bge	$s0, $s1, b
	ble	$s0, $s1, c
	beq 	$s0, $s1, d
	blt	$s0, $s1, e
	addi	$s1, $s1, 1
	
	
	a:
	addi 	$s0, $s0, 1
	j 	exit
	
	b:
	addi 	$s1, $s1, 1
	j 	exit
	
	c:
	addi 	$s0, $s0, 1
	j 	exit
	
	d:
	add	$s1, $s0, 0
	j 	exit
	
	e:
	addi 	$s0, $s0, 1
	j 	exit
	
	
	
	exit: