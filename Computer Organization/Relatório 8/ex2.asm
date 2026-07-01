.data

# ----- Definindo variáveis -----

	MAX:		.word	6	# tamanho da matriz
	block_size:	.word	3	# tamanho do bloco
	
.text

# ----- Início de variáveis -----

main:
	lw	$s2, MAX		# salva MAX em $s2
	lw	$s3, block_size		# salva block_size em $s3
	
	# --- Cria matrizes ----
	
	move	$a0, $s2		# parametro da função = max
	jal	cria_matriz
	move	$s0, $v0		# salva matriz A em $s0
	
	move	$a0, $s2		# parametro da função = max
	jal	cria_matriz
	move	$s1, $v0		# salva matriz B em $s1
	
# ----- Inicialização de loops -----

	li	$t0, 0			# i = 0
	
for_i:
	bge	$t0, $s2, exit		# if (i >= MAX): encerra programa
	
	li 	$t1, 0			# j = 0

for_j:
	bge	$t1, $s2, end_for_j	# if (j >= MAX): volta pro for_i
	
	move	$t2, $t0		# ii = i
	
for_ii:
	add	$t4, $t0, $s3		# var_temp = i + block_size
	bge	$t2, $t4, end_for_ii	# if (ii >= i+block_size): volta pra for_j
	
	move	$t3, $t1		# jj = j
	
for_jj:
	add	$t5, $t1, $s3		# var_temp = j + block_size
	bge	$t3, $t5, end_for_jj	# if (jj >= j + block_size): volta pro for_ii
	
	
        # ----- Cálculo de soma de matrizes dentro do loop -----
	
	# - Calculando endereço de A[ii][jj] -
	
	mul	$t6, $t2, $s2		# $t6 = ii * MAX
	add	$t6, $t6, $t3		# $t6 = ii * MAX + jj
	sll	$t6, $t6, 2		# $t6 = (ii * MAX + jj) * 4 (tam word)
	add	$t6, $t6, $s0		# $t6 = endereço final A[ii][jj]
	
	# - Carrega A[ii][jj] -
	
	lw	$t7, 0($t6)
	
	# - Calculando endereço de B[jj][ii] -
	
	mul	$t8, $t3, $s2		# $t6 = jj * MAX
	add	$t8, $t8, $t2		# $t6 = jj * MAX + ii
	sll	$t8, $t8, 2		# $t6 = (jj * MAX + ii) * 4 (tam word)
	add	$t8, $t8, $s1		# $t6 = endereço final B[jj][ii]
	
	# - Carrega B[jj][ii] -
	
	lw	$t9, 0($t8)
	
	# - Soma A[ii][jj] + B[jj][ii] -
	
	add	$s4, $t7, $t9 		# $s4 = A[ii][jj] + B[jj][ii]
	sw	$s4, 0($t6)		# armazena de volta em A[ii][jj]
	
	# ---------------------------------------------------------------
	
# ----- Finalização de loops -----

	addi	$t3, $t3, 1		# jj++
	j	for_jj			# volta pro loop
	
end_for_jj:
	addi	$t2, $t2, 1		# ii++
	j	for_ii
	
end_for_ii:
	add	$t1, $t1, $s3		# j += block_size
	j	for_j
	
end_for_j:
	add	$t0, $t0, $s3		# i += block_size
	j	for_i
	
exit:
	li	$v0, 10
	syscall
	
# ----- Função geradora de matrizes (alocação dinamica na memória heap) -----

cria_matriz:

	li 	$t0, 0					# inicia row como 0
	li	$t2, 1					# inicia value como 0
	move	$t3, $a0				# salva o tamanho da matriz (MAX) em $t3
	
	# --- calculando espaço necessário para alocar (max * max * 4) salva em $t5 ---
	
	mul	$t5, $t3, $t3				# calcula max * max
	sll 	$t5, $t5, 2				# multiplica pelo tamanho da word (4 bytes)
	
	# --- aloca espaço dinamicamente na matriz ---
	
	li 	$v0, 9                   # syscall que serve para criar um espaço para alocação na memória heap
    	move 	$a0, $t5                 # envia para o syscall quantos bytes serão alocados
    	syscall				 # endereço alocado está salvo em $v0 (que é o retorno da própria função cria_matriz)
	
	
	loop_out:
		li	$t1, 0				# reseta a coluna para 0

		loop_in:
			# --- calculando o offset (distancia do endereço base ao dado atual) = ( linha * max + coluna ) * tam_word ---
			 
			mul 	$t4, $t0, $t3		# offset ($t4) = linha * max
			add 	$t4, $t4, $t1		# offset += coluna
			sll 	$t4, $t4, 2		# offset *= 4 (fazendo isso pois estamos trabalhando com word = 4 bytes)
			add 	$t4, $v0, $t4       	# endereço = end. base + offset

			# --- mexendo com a matriz ---
			
			sw 	$t2, 0($t4)		# armazena value na posição da matriz
			addi 	$t2, $t2, 1		# value += 1
			addi 	$t1, $t1, 1		# coluna += 1
			bne  	$t1, $t3, loop_in	# verificamos se coluna < max, caso contrário repetimos o loop interno

			addi 	$t0, $t0, 1		# linha += 1
			bne 	$t0, $t3, loop_out  	# pula para o loop de fora
	
	jr 	$ra
