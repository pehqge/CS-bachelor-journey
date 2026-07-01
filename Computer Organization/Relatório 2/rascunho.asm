.data
segmentos:
.byte 0b00111111   # 0
.byte 0b00000110   # 1
.byte 0b01011011   # 2
.byte 0b01001111   # 3
.byte 0b01100110   # 4
.byte 0b01101101   # 5
.byte 0b01111101   # 6
.byte 0b00000111   # 7
.byte 0b01111111   # 8
.byte 0b01101111   # 9

.text

#descobrir

# Configurar o endereço base do display de 7 segmentos
li $t0, 0x(endereçoseila)

# Loop para exibir os números de 0 a 9
li $t1, 0      # Inicializa contador com 0

loop:
# Escrever o padrão de segmentos correspondente ao número atual

1- carregar
2 - escrever