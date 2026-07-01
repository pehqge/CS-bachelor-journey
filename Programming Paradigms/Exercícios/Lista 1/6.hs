triangulo :: Int -> Int ->  Int -> Bool
triangulo a b c = (a + b > c) && (a + c > b) && (b + c > a)

main = do
    putStrLn "Escreva três inteiros para o tamanho do triangulo: "
    x <- getLine
    y <- getLine
    z <- getLine
    
    let nX = (read x :: Int)
    let nY = (read y :: Int)
    let nZ = (read z :: Int)

    let verdade = triangulo nX nY nZ
    if verdade then putStrLn "Pode sim construir um triangulo" else putStrLn "Não pode construir"
    
