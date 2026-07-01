main = do
    putStrLn "Informe dois numeros: "
    nA <- getLine
    nB <- getLine
    
    -- converte para float
    let numA = (read nA :: Float)
    let numB = (read nB :: Float)
    
    -- imprime exponenciacao
    print (numA**numB)