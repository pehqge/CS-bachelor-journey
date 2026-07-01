# nessa, crio um dicionario para armazenar todos os presentes numa lista que a pessoa quer. Em que a pessoa é a chave e a lista é o valor.
# depois vou interando sobre o dicionario para ver se a pessoa acertou no presente ou não.
# se a pessoa acertou, imprime uhul
# caso ao contrario, ou se a pessoa não existir no dicionario, "tente novamente"

x = int(input())
dic = {}
for i in range(x):
    n, p1, p2, p3 = input().split()
    dic[n] = [p1, p2, p3]
while True:
    try:
        n, p = input().split()
        if n in dic.keys():
            if p in dic[n]:
                print("Uhul! Seu amigo secreto vai adorar o/")
            else:
                print("Tente Novamente!")
        else:
                print("Tente Novamente!")
                
    except EOFError:
        break