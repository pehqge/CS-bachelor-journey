.data
	A: 	.word 10
	B: 	.word 15
	C: 	.word 20
	D: 	.word 25
	E: 	.word 30
	F: 	.word 35
	
	G:	 .word 0, 0, 0, 0
	H:	 .word 0, 0, 0, 0
	
.text
# salvando dados da memoria nos regs
	lw	$s0, A
	lw	$s1, B
	lw	$s2, C
	lw	$s3, D
	lw	$s4, E
	lw	$s5, F
	
	la	$s6, G
	la	$s7, H
	
# a) G[0] = (A – (B + C) + F)
	add	$t0, $s1, $s2
	sub	$t0, $s0, $t0
	add 	$t0, $t0, $s5
	sw	$t0, 0($s6)
	
# b) G[1] = E – (A – B) * (B – C)
	sub	$t0, $s0, $s1	# A - B
	sub	$t1, $s1, $s2	# B - C
	mul	$t0, $t0, $t1	# (A - B) * (B - C)
	sub	$t0, $s4, $t0	# E - (A - B) * (B - C)
	sw	$t0, 4($s6)
	
