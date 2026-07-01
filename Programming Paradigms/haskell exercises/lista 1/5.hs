media :: Float -> Float -> Float -> Float
media a b c = (a + b + c) / 3

aprovacao :: Float -> String
aprovacao a = if a >= 6 then "O aluno foi aprovado" else "O aluno foi reprovado"

main = do
    putStrLn "Informe 3 notas:"
    a <- getLine
    b <- getLine
    c <- getLine
    let nA = (read a :: Float)
    let nB = (read b :: Float)
    let nC = (read c :: Float)

    putStrLn (aprovacao (media nA nB nC))
