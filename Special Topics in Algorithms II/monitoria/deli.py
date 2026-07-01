l, n = input().split()
l = int(l)
n = int(n)

#listas que armazenam o singular e o plural de cada palavra
sl = []
pl = []

#lendo as palavras irregulares
for _ in range(l):
    singular, plural = input().split()
    sl.append(singular)
    pl.append(plural)

for _ in range(n):
    palavra = input().strip() #strip tira espaços
    palavra_plural = palavra #inicialmente a palavra no plural é a mesma que no singular

# confere se ela é irregular
    if palavra in sl: 
        index = sl.index(palavra) # se for, pega o índice da palavra no singular
        palavra_plural = pl[index] # salva o plural correspondente


    else: # entra no else se for regular
        tamanho = len(palavra)

        if tamanho > 1 and palavra[tamanho - 1] == 'y' and palavra[tamanho - 2] not in 'aeiou':
            palavra_plural = palavra[:tamanho - 1] + 'ies'

        elif palavra.endswith('o') or palavra.endswith('s') or palavra.endswith('ch') or palavra.endswith('sh') or palavra.endswith('x'):
            palavra_plural = palavra + 'es'

        else:
            palavra_plural = palavra + 's'

    print(palavra_plural)