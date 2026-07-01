while True:
    proibido = ".,!? "
    frase = ""
    
    inputt = input()
    
    if inputt == "DONE":
        break
    
    for i in inputt:
        if not i in proibido:
            frase += i.lower()
            
    if frase == frase[::-1]:
        print("You won't be eaten!")
    else:
        print("Uh oh..")