# nessa eu utilizo a funcao .format do python que automaticamente formata o numero na casa de 3.
# depois concateno ao valor formatado o $ e os centavos com precisao de 2 casas

while True:
    try:
        dolar = int(input())
        centavo = int(input())
        valor = "{:,}".format(dolar)
        total = "$"+valor+f".{centavo:02d}"
        print(total)

    except EOFError:
        break