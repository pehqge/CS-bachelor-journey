.data

# criando uma estrutura para salvar os números de 0 a 9 em hexadecimal
numero:
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

.text
main:
    	li 	$t0, 0          	# contador (inicializado com 0)
    	li 	$s0, 0xFFFF0010		# salvando o endereço do display na memoria
    
loop:
	li	$t2, 0
    	lw 	$t1, numero($t0)     	# carregando o numero que será mostrado no display (de acordo com o contador)
    	sb 	$t1, 0($s0)		# envia o número para o display
    	
temporizador:
    	addi	$t2, $t2, 1		# incrementa temporizador
    	bne	$t2, 40000, temporizador	
    
    	addi 	$t0, $t0, 4         	# incrementa o contador em 4 para acessar o próximo numero a ser exibido
    	bne 	$t0, 40, loop        	# repete até que todos os números de 0 a 9 tenham sido exibidos (contador < 10*4)
    
j main # se acabou, ele volta pro começo pra fazer um novo ciclo de 0 a 9

