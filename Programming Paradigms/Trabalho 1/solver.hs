import Data.Array 
import Data.List 
import Data.Map (Map) 
import qualified Data.Map as Map

----- * definicoes de modelagem do puzzle * -----

type Pos = (Int, Int)       -- posicao (linha, coluna)
type Grid = Array Pos Int   -- tabuleiro do jogo
type RegionMap = Array Pos Int   -- mapeia cada posicao para uma regiao
type Regions = Map Int [Pos]     -- mapeia cada regiao para uma lista de posicoes


width, height :: Int
width = 17
height = 17

-- grid inicial 
initialGrid :: Grid
initialGrid = listArray
  ((1, 1), (height, width)) 
  [0, 0, 3, 0, 2, 0, 3, 0, 0, 0, 7, 0, 0, 5, 0, 3, 6, 0, 0, 0, 0, 0, 2, 0, 6, 0, 2, 0, 0, 3, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 4, 0, 5, 1, 0, 2, 0, 0, 0, 3, 0, 7, 0, 0, 5, 0, 0, 0, 0, 0, 7, 4, 0, 2, 0, 0, 2, 1, 0, 2, 0, 0, 0, 3, 0, 5, 0, 0, 6, 0, 0, 0, 1, 0, 3, 4, 0, 0, 0, 3, 0, 0, 0, 3, 0, 5, 0, 0, 0, 3, 3, 1, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 5, 2, 6, 0, 0, 0, 0, 1, 0, 1, 0, 2, 0, 6, 0, 0, 5, 0, 0, 2, 0, 5, 0, 5, 0, 7, 0, 3, 0, 4, 0, 0, 0, 0, 0, 7, 0, 3, 0, 2, 3, 0, 0, 4, 0, 0, 3, 1, 5, 0, 3, 0, 5, 0, 6, 0, 0, 4, 0, 4, 0, 3, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 4, 0, 5, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 1, 0, 0, 4, 0, 5, 0, 6, 3, 4, 0, 4, 5, 0, 6, 2, 0, 0, 1, 4, 0, 3, 0, 0, 2, 0, 0, 0, 0, 3, 0, 4, 0, 3, 0, 6, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 6, 2, 0, 0, 1, 3, 1, 7, 1, 2, 0, 4, 0, 4, 1, 0, 6]

-- rotulos das regioes
regionMap :: RegionMap
regionMap = listArray
    ((1, 1), (height, width))
    [1, 9, 9, 9, 9, 23, 18, 28, 28, 38, 41, 41, 48, 48, 55, 56, 56, 2, 10, 10, 14, 18, 18, 18, 29, 29, 29, 41, 41, 41, 48, 48, 56, 56, 2, 2, 14, 14, 19, 19, 19, 29, 29, 29, 41, 41, 48, 48, 56, 56, 56, 3, 3, 15, 15, 15, 19, 19, 30, 30, 33, 33, 33, 33, 45, 45, 59, 59, 3, 3, 15, 15, 20, 24, 19, 30, 30, 33, 39, 44, 45, 45, 52, 60, 59, 4, 11, 15, 15, 20, 24, 24, 24, 33, 33, 39, 45, 45, 52, 52, 60, 60, 5, 11, 11, 5, 20, 25, 25, 24, 34, 39, 39, 46, 45, 52, 52, 57, 63, 5, 5, 5, 5, 5, 21, 25, 25, 34, 39, 39, 46, 46, 52, 57, 57, 58, 6, 12, 12, 12, 21, 21, 21, 25, 34, 40, 40, 40, 49, 49, 57, 58, 58, 6, 6, 12, 16, 16, 21, 21, 25, 31, 40, 40, 40, 50, 49, 58, 58, 58, 6, 6, 12, 16, 16, 16, 27, 31, 31, 31, 42, 40, 50, 50, 50, 50, 61, 6, 6, 12, 12, 22, 16, 27, 27, 35, 35, 42, 42, 42, 50, 53, 61, 61, 7, 13, 13, 17, 22, 16, 27, 27, 36, 35, 35, 42, 42, 53, 53, 53, 53, 7, 7, 13, 17, 22, 22, 26, 27, 37, 35, 35, 43, 51, 51, 53, 62, 62, 7, 7, 13, 17, 17, 26, 26, 32, 37, 37, 43, 43, 43, 51, 54, 62, 62, 7, 7, 8, 8, 17, 26, 26, 32, 37, 37, 43, 47, 47, 51, 54, 54, 64, 8, 8, 8, 8, 17, 17, 26, 26, 37, 37, 43, 43, 47, 54, 54, 54, 54]

-- mapeia de um jeito que a chave é o numero da regiao e o valor eh um array com todas tuplas de posicao (x, y) que pertencem a regiao
regions :: Regions
regions = Map.fromListWith (++)
  [ (regionMap ! (x, y), [(x, y)]) | x <- [1..width], y <- [1..height] ]


----- * algoritmo de solving * -----

main :: IO ()
main = case solve initialGrid of
  Just solution -> displayGrid solution  -- mostra a solucao caso ache
  Nothing       -> putStrLn "Nenhuma solução encontrada"  -- se contrario, avisa q n encontrou


solve :: Grid -> Maybe Grid
solve grid = solver grid (1, 1)  -- comeca resolvendo pela posicao (1,1)

-- funcao recursiva principal 
solver :: Grid -> Pos -> Maybe Grid
solver grid (y, x)
  | y > height          = Just grid  -- quando o y eh maior q a altura, chegou ao fim (deu certo!)
  | x > width           = solver grid (y + 1, 1)  -- x maior q a largura, avanca para a proxima linha
  | grid ! (y, x) /= 0  = solver grid (y, x + 1)  -- se a celula ja esta preenchida, avanca para a proxima celula
  | otherwise           = -- senao, tenta preencher a celula
      let options = availableNumbers grid (y, x)  -- recebe todos os numeros possiveis que encaixam nessa celula
      in tryOptions grid (y, x) options  -- tenta cada opcao disponivel para a celula

-- testa recursivamente cada opcao disponivel para a celula
tryOptions :: Grid -> Pos -> [Int] -> Maybe Grid -- recebe o grid, a posicao e a lista de opcoes disponiveis
tryOptions _ _ [] = Nothing  -- se nao ha mais opcoes, retorna Nothing 
tryOptions grid pos (n:ns) = -- pega o primeiro elemento da lista = n e o resto da lista = ns
  case solver (grid // [(pos, n)]) (fst pos, snd pos + 1) of  -- atualiza o grid com o novo numero e avanca para a proxima coluna
    Just result -> Just result  -- se encontrou uma solucão, retorna o grid completo
    Nothing     -> tryOptions grid pos ns  -- se nao achou, tenta a proxima opcao da lista

-- obtem as opcoes de numeros disponiveis para a celula
availableNumbers :: Grid -> Pos -> [Int]
availableNumbers grid pos =
  let adjNums = adjacentNumbers grid pos  -- numeros vizinhos da celula (nao podem ser iguais a celula)
      regNums = regionNumbers grid pos    -- numeros da regiao da celula (nao pode repetir algum que ja esta la)
      validNums = validNumbers grid pos   -- numeros que podem ser usados pela regra da verticalidade do jogo (o numero tem que ser menor que o de baixo e maior que o de cima, se for da mesma regiao)
      forbiddenNums = nub $ adjNums ++ regNums  -- pega os numeros unicos que nao podem ser usados (vizinhos e regiao)
  in validNums \\ forbiddenNums  -- o que pode ser usado: numeros validos da verticalidade - numeros proibidos

-- retorna os vizinhos da celula
adjacentNumbers :: Grid -> Pos -> [Int]
adjacentNumbers grid (y, x) =
  [ grid ! p | p <- [(y-1,x),(y+1,x),(y,x-1),(y,x+1)]  -- posicoes vizinhas
             , inBounds p, grid ! p /= 0 ]  -- verificacao se é diferente de 0 e se nao esta passando do limite do grid

-- retorna os numeros presentes naquela regiao
regionNumbers :: Grid -> Pos -> [Int]
regionNumbers grid pos =
  [ grid ! p | p <- regions Map.! (regionMap ! pos), grid ! p /= 0 ]  -- retorna os numeros da grid que estao dentro da mesma regiao da celula e sao diferentes de 0

-- retorna os numeros validos para a celula de acordo com a regra da verticalidade
validNumbers :: Grid -> Pos -> [Int]
validNumbers grid pos =
  let lower = getNeighborValue grid pos (y + 1, x) 0  -- pega o valor do vizinho de baixo da mesma regiao (se nao tiver, retorna 0)
      upper = getNeighborValue grid pos (y - 1, x) (regionSize pos + 1)  -- pega o valor do vizinho de cima da mesma regiao (se nao tiver, retorna o tamanho da regiao + 1 como limite superior)
      from = lower + 1  -- tem que ser pelo menos 1 maior que o de baixo
      to = upper - 1    -- tem que ser pelo menos 1 menor que o de cima
  in if from <= to then [from..to] else []  -- lista com todos os numeros validos, se nao tiver, retorna uma lista vazia
  where (y, x) = pos  -- define as coordenadas da celula 

-- retorna o valor do vizinho desejado da mesma regiao, se nao tiver, retorna um valor padrao
getNeighborValue :: Grid -> Pos -> Pos -> Int -> Int
getNeighborValue grid pos neighbor defaultValue
  | inBounds neighbor && regionMap ! pos == regionMap ! neighbor = -- se o vizinho está dentro dos limites e na mesma regiao
      let val = grid ! neighbor
      in if val /= 0 then val else defaultValue  -- se o vizinho ja esta preenchido, retorna o valor dele, senao, retorna o valor padrao
  | otherwise = defaultValue -- se nao, retorna o valor padrao

-- calcula o tamanho da regiao da celula
regionSize :: Pos -> Int
regionSize pos = length (regions Map.! (regionMap ! pos))  

-- verifica se a posicao esta dentro dos limites da grid
inBounds :: Pos -> Bool
inBounds (y, x) = y >= 1 && y <= height && x >= 1 && x <= width  

-- exibe o grid
displayGrid :: Grid -> IO ()
displayGrid grid = mapM_ printRow [1..height]  
  where
    printRow y = putStrLn $ unwords [showCell (grid ! (y, x)) | x <- [1..width]]  
    showCell n = if n == 0 then "-" else show n  