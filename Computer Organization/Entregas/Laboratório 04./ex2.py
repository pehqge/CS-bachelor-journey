def fatorial(x):
    if (x == 0):
        return 1
    else:
        return x * fatorial(x-1)
    
def potencia(x, n):
    valor = 1
    for _ in range(n):
        valor *= x
        
    return valor
    
def seno(x):
    # somatoria de     (((-1)**n) / (2*n + 1)! ) *  x**(2*n + 1)
    # vou chamar de:   ( (sinal)  /   (fat)!   ) *   (x**fat)  )
    # vou chamar de:   (      (fator)            *     (x2)    ) = interno
    #                  seno += interno
    
    seno = 0
    
    for n in range(20):
        sinal = potencia(-1, n) # sinal
            
        # calculando fat = (2*n + 1)
        fat = n + n
        fat += 1
        
        # fator = sinal / (2*n + 1)!
        fator = fatorial(fat)
        fator = sinal / fator
        
        # x2 = x ** (2*n + 1)
        x2 = potencia(x, fat)
        
        # seno += a iteracao interna
        interno = fator * x2
        seno += interno
        print(seno)
        
    return seno
            
    
def main():
    x = float(input("Digite o número para calcular o seno (em radianos): "))
    resultado_aproximado = seno(x)
    print(f"O valor aproximado do seno de {x} radianos é: {resultado_aproximado}")
    
if __name__ == "__main__":
    main()