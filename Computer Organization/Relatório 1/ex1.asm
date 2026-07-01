# Programa para calcular:
# a = b + 35
# c = d - a + e

.data # Armazenando as variaveis na memoria de dados

	A: .word 0 # iniciada com 0 pois sera atribuido o valor posteriormente
	B: .word 15
	C: .word 0
	D: .word 20
	E: .word 25
	
	# strings para imprimir no console
	valorA: .asciiz "Valor de A após operação (B + 35): "
	newline: .asciiz "\n"
	valorC: .asciiz "Valor de C após operação (D - A + E): "

.text
	# ---- alocando variaveis no registrador -----
	la	$s0, A  
	la	$s1, B
	la	$s2, C
	la	$s3, D
	la	$s4, E
	
	# ---- 1a operacao A = B + 35 -----
	lw	$t1, 0($s1) # carregando temp B
	addi	$t0, $t1, 35 # salvando B + 35 em temp A
	sw	$t0, 0($s0) # carregando temp A no registrador destino na mem
	
	# --- imprimindo resultado de A ----
	
	# imprimindo string para A
	li	$v0, 4
	la	$a0, valorA
	syscall
	
	# imprimindo A
	li	$v0, 1
	li	$a0, 0
	add	$a0, $a0, $t0
	syscall
	
	# imprimindo nova linha
	li	$v0, 4
	la	$a0, newline
	syscall
	
	# ---- 2a operacao C = D - A + E -----
	lw	$t3, 0($s3) # carregando D
	lw	$t4, 0($s4) # carregando E
	
	sub	$t2, $t3, $t0 # carregando D - A em temp C
	add	$t2, $t2, $t4 # carregando resultado anterior + E em temp C
	
	sw	$t2, 0($s2) # salvando o resultado em C
	
	# ---- imprimindo resultado de C -----
	
	# imprimindo string de C
	li	$v0, 4
	la	$a0, valorC
	syscall
	
	# imprimindo C
	li	$v0, 1
	li	$a0, 0 # limpando a0
	add	$a0, $a0, $t2
	syscall