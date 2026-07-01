.data

# ----- Definindo variável -----

	MAX:		.word	4	# tamanho da matriz
	
.text

# ----- Início de variáveis -----

main:
	lw	$s2, MAX		# salva MAX em $s2
	
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
	
	li	$t1, 0			# j = 0
	
for_j:
	bge	$t1, $s2, end_for_j	# if (j >= MAX): volta pro for_i
	
	# ----- Cálculo de soma de matrizes dentro do loop -----
	
	# - Calculando endereço de A[i][j] -
	
	mul 	$t2, $t0, $s2   	# $t2 = i * MAX
    	add 	$t2, $t2, $t1   	# $t2 = i * MAX + j
    	sll 	$t2, $t2, 2      	# $t2 = (i * MAX + j) * 4 (endereço de A[i][j])
    	add 	$t2, $t2, $s0    	# endereço final de A[i][j] = base(A) + offset
    	
    	# - Carrega A[i][j] -
    
    	lw 	$t3, 0($t2)

    	# - Calculando o endereço de B[j][i] -
    	
    	mul 	$t4, $t1, $s2    	# $t4 = j * MAX
    	add 	$t4, $t4, $t0    	# $t4 = j * MAX + i
    	sll 	$t4, $t4, 2      	# $t4 = (j * MAX + i) * 4 (endereço de B[j][i])
    	add 	$t4, $t4, $s1    	# endereço final de B[j][i] = base(B) + offset

    	# - Carregando o valor de B[j][i] - 
    	
    	lw 	$t5, 0($t4)

   	# - Soma A[i][j] + B[j][i] -
   	
    	add 	$t3, $t3, $t5
    	sw 	$t3, 0($t2)		# Armazena o resultado de volta em A[i][j]
    	
# ----- Finalização de loops -----

	addi	$t1, $t1, 1		# j++
	j	for_j			# volta pro loop
	
end_for_j:
	add	$t0, $t0, 1		# i++
	j	for_i			# volta pro loop
	
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
	
	li 	$v0, 9                   		# syscall que serve para criar um espaço para alocação na memória heap
    	move 	$a0, $t5                 		# envia para o syscall quantos bytes serão alocados
    	syscall				 		# endereço alocado está salvo em $v0 (que é o retorno da própria função cria_matriz)
	
	
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

	
	
