.text
	j main
	
calculaAreaQuadrado:
	mul	$v0, $a0, $a1
	jr	$ra

main:
	li	$a0, 4
	li	$a1, 10
	jal	calculaAreaQuadrado
	move	$s0, $v0
	