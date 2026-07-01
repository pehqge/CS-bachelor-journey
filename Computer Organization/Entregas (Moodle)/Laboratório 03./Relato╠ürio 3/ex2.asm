.data
    RESULTADO: .word 0
    N: .word 5
    vetor: .word 11, 2, 3, 14, 15

.text

j main

soma:
    add $t0, $t0 0           # Inicia o acumulador em 0
    beq $a1, $zero, fim_soma   # Se N for igual a zero, termina a soma
    lw $t2, 0($a0)		#carrega o conteúdo que está no registrador (próximo elemento do vetor)
    add $t0, $t0, $t2   # Adiciona o valor do vetor ao acumulador
    addi $a1, $a1, -1   # Decrementa o argumento N 
    addi $a0, $a0, 4    # Atualiza o endereço base do vetor para o próximo elemento
    addi $sp, $sp, -4
    sw $ra, 0($sp)
    jal soma            # Chama a função recursivamente
    addi $sp, $sp, 4
    lw $ra 0($sp)
    jr $ra              # Retorna

fim_soma:
    move $v0, $t0       # Move o resultado para $v0
    jr $ra              # Retorna

main:

	# ----- salvando dados da mem�ria -----

    la $s0, RESULTADO      # Carrega o endereço base do vetor em $s0
    la $s1, N           # Carrega o endereço de N em $a1

	# ----- armazenando os argumentos da fun��o em a0 e a1 -----
    la $a0, vetor       #carrega o conteúdo do endereço base no registrador argumento da função
    lw $a1, 0($s1)
	# ----- chamando a funcao -----
    jal soma            # Chama a função soma
	# ----- armazena o resultado da soma -----    
    sw $v0, 0($s0)  # Armazena o resultado na memória