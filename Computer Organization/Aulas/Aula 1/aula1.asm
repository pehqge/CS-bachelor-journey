# Programa para interpretar A = B + C; em que B = 5 e C = 3

.data # parte do arquivo para variaveis

	A: .word 0 # inicando variavel
	B: .word 5
	C: .word 3
	
.text

	# load address eh usado pois nao se sabe onde ele salvou em .data
	
	la	$s0, A  # alocando variavel no registrador (load address), guarda o endereco
	la	$s1, B
	la	$s2, C
	
	lw	$t0, 0($s1) # colocando num registrador temporario para fazer operacoes (guarda o conteudo como ponteiro)
	lw	$t1, 0($s2) # o 0 eh usado aqui pois represta um endereco apenas, com mais seria um vetor
	
	add	$t3, $t0, $t1 # somando t0 + t1 e alocando em t3 para nao matar o endereco de s0
	
	sw	$t3, 0($s0)