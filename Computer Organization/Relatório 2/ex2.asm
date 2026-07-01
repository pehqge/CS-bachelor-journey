.data

# armazenando em estruturas as linhas a serem lidas, 
# os valores possíveis que o teclado pode retornar 
# e os códigos para aparecer no display
	
valor_teclado:
	.word	0x11			# tecla 0
	.word 	0x21   	 		# tecla 1
	.word 	0x41   	 		# tecla 2
	.word 	0x81   	 		# tecla 3
	.word 	0x12    		# tecla 4
	.word 	0x22   	 		# tecla 5
	.word 	0x42    		# tecla 6
	.word 	0x82    		# tecla 7
	.word 	0x14    		# tecla 8
	.word 	0x24    		# tecla 9
	.word 	0x44    		# tecla A
	.word 	0x84    		# tecla B
	.word 	0x18    		# tecla C
	.word 	0x28    		# tecla D
	.word 	0x48    		# tecla E
	.word 	0x88    		# tecla F
	
numero_7seg:
	.word	0x3F   			# 0
    	.word 	0x06   			# 1
    	.word 	0x5B   			# 2
    	.word 	0x4F   			# 3
    	.word 	0x66  			# 4
   	.word 	0x6D  			# 5
    	.word 	0x7D  			# 6
   	.word 	0x07   			# 7
   	.word 	0x7F  			# 8
   	.word 	0x6F   			# 9
   	.word 	0x77   			# A
   	.word 	0x7C   			# B
   	.word 	0x39   			# C
   	.word 	0x5E   			# D
   	.word 	0x79   			# E
   	.word 	0x71   			# F

.text

	li 	$s0, 0xffff0010		# salva endereço do display de 7 segmentos
	li 	$s1, 0xffff0012		# salva endereço do selecionador de linhas
	li 	$s2, 0xffff0014		# salva endereço do receptor de leitura do teclado

main:	

	li	$t1, 1			# $t1 recebe a linha a ser lida (1a linha)
	
row_check:

	sb 	$t1, 0($s1)		# armazena no selecionador a linha a ser inspecionada
	lw 	$t2, 0($s2)		# $t2 recebe o valor recebido pelo teclado naquela linha
	
	bnez 	$t2, key_event		# se o registrador $t2 tiver algum valor dentro, uma tecla foi pressionada e vai para o gerenciador
	
	add	$t1, $t1, $t1		# incrementa para a proxima linha ser lida
	beq	$t1, 16, main		# se passar da 4a linha, volta para linha 1
	
	j	row_check		# se nenhuma tecla foi pressionada, o ciclo reinicia para a próxima linha
	
key_event:				# evento de tratamento ao pressionar tecla

	li	$t3, 0			# inicia o contador_posição para saber qual tecla foi apertada para imprimir no 7seg 
	
key_find:				# loop para encontrar qual tecla foi pressionada e colocar seu numero no display

	lw	$t4, valor_teclado($t3) # $t4 recebe um valor de tecla para, posteriormente, comparar do .data com a tecla pressionada
	beq	$t4, $t2, display_print # se a tecla for igual a pressionada, irá para o evento de imprimir o valor no display 7seg
	
	addi	$t3, $t3, 4		# soma o contador para ir para a proxima tecla a verificar
	beq	$t3, 64, key_event	# se o contador atingir o valor máximo, ele retorna para o inicio da contagem
	
	j 	key_find		# volta para o loop para verificar a proxima tecla
	
display_print:

	li	$t6, 0			# inicia contador para um temporizador para o display não ficar piscando
	lw	$t5, numero_7seg($t3)	# $t5 recebe o valor para colocar no display 7 seg correspondente a qual tecla foi apertada
	
	sb 	$t5, 0($s0)		# imprime no display 7seg o valor da tecla
	
temporizador:				
	
	addi	$t6, $t6, 1		# incrementa o temporizador
	bne	$t6, 1000, temporizador # após passar o temporizador, ele volta para a main
	
	j	main			#volta para a função main, a fim de repetir o processo para exibir o próximo número
