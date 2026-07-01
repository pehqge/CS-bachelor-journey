-- Crie uma funcao que receba um numero x, negativo ou positivo, e retorne seu valor absoluto. Leia x do teclado.

absoluto :: Int -> Int
absoluto x = if x < 0 then -x else x

main = do
    putStrLn "Informe um numero: "
    n <- getLine
    let num = (read n :: Int)
    print (absoluto num)