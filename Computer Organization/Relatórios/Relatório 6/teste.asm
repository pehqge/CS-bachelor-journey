.data
matrix: .space 1024  # Espaço para a matriz 16x16, cada elemento tem 4 bytes (inteiro)
value:  .word 0      # Inicializa a variável value com 0

.text
.globl main

main:
    la $t0, matrix    # Carrega o endereço base da matriz em $t0
    lw $t1, value     # Carrega o valor inicial de 'value' em $t1
    li $t2, 0         # Inicializa o contador de linhas (row) em $t2

outer_loop:
    li $t3, 0         # Inicializa o contador de colunas (col) em $t3

inner_loop:
    mul $t4, $t2, 16  # Calcula o offset da linha: row * 16
    add $t4, $t4, $t3 # Adiciona o offset da coluna: (row * 16) + col
    sll $t4, $t4, 2   # Multiplica o offset por 4 (tamanho do inteiro)
    add $t5, $t0, $t4 # Calcula o endereço do elemento da matriz

    sw $t1, 0($t5)    # Armazena o valor em matrix[row][col]
    addi $t1, $t1, 1  # Incrementa o value

    addi $t3, $t3, 1  # Incrementa o col
    li $t6, 16
    bne $t3, $t6, inner_loop # Se col < 16, continua no inner_loop

    addi $t2, $t2, 1  # Incrementa o row
    li $t7, 16
    bne $t2, $t7, outer_loop # Se row < 16, continua no outer_loop

    # Programa finalizado
    li $v0, 10         # Código do syscall para finalizar o programa
    syscall
