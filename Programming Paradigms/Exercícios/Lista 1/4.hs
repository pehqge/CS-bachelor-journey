-- Crie uma funcao que faca xor entre dois valores booleanos

ouExclusivo :: Bool -> Bool -> Bool
ouExclusivo a b = (a && not b) || (not a && b)

main = do
    putStrLn "Coloque um valor booleano:"
    a <- getLine
    let boolA = (read a :: Bool)
    putStrLn "Coloque outro valor booleano:"
    b <- getLine
    let boolB = (read b :: Bool)
    putStrLn "O xor entre os dois é:"
    print (ouExclusivo boolA boolB)