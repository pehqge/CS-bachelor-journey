        sub $s0,$s0,$s0        # Limpa o registrador $s0 para garantir que inicia com 0, pois pode ser iniciado com um valor indefinido
        lui $s1,0xffff         # Carrega o valor imediato 0xffff nos 16 bits mais significativos de $s1 (registrador de base para I/O)

main:
        li $s3, 0x01           # Inicializa um registrador para representar a primeira linha do teclado matricial
	li $s5, 0xFFFF0010 	#salva o endereço do display na memória
loop_rows:
        sb $s3, 0x0012($s1)    # Seleciona a linha correspondente do teclado matricial. Lembrando que o endereço 0x0012 capta a linha
        lb $s4, 0x0014($s1)    # Lê os dados do teclado matricial e armazena em s4
        
        # Verifica se alguma tecla foi pressionada nesta linha
        bne $s4, $s0, handle_keypress
        
        # Se nenhuma tecla foi pressionada, passa para a próxima linha
        add $s3, $s3, $s3       # Desloca $s3 para a próxima linha (1, 2, 4, 8)
        beq $s3, 16, main
        
        bnez $s3, loop_rows    # Se $s3 não é zero, continua para a próxima linha
                               # Se $s3 for zero, termina o loop (todas as linhas foram lidas)

        j main                 # Retorna ao início do loop principal

handle_keypress: #se alguma tecla foi pressionada, o bne pula para cá

	sb $s4, 0($s5) #envia o numero para o display
	


