-- Crie uma funcao que calcule a area de um triangulo

areaTriangulo :: Float -> Float -> Float
areaTriangulo a b = (a * b) / 2

main = do
    putStrLn "Informe uma base:"
    b <- getLine
    let base = (read b :: Float)
    putStrLn "Informe uma altura:"
    a <- getLine
    let altura = (read a :: Float)
    print (areaTriangulo altura base)