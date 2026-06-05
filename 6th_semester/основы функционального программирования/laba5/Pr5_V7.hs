module Main where

pascal :: [[Integer]]
pascal = [1] : map nextRow pascal
  where
    nextRow :: [Integer] -> [Integer]
    nextRow row = zipWith (+) (0 : row) (row ++ [0])

-- [0,1,2,1] [1,2,1,0] = [1,3,3,1].

-- pascalRow — n-я строка треугольника (нумерация с 0)

pascalRow :: Int -> [Integer]
pascalRow n = pascal !! n

-- pascalAt — элемент (строка, столбец) = биномиальный коэффициент C(n,k)

pascalAt :: Int -> Int -> Integer
pascalAt n k
  | k < 0 || k > n = 0
  | otherwise = pascalRow n !! k

-- binomial — биномиальный коэффициент C(n,k) через pascalAt

binomial :: Integer -> Integer -> Integer
binomial n k = pascalAt (fromInteger n) (fromInteger k)

-- main — демонстрация и проверка

main :: IO ()
main = do
  putStrLn "Первые 6 строк треугольника Паскаля:"

  mapM_ print (take 6 pascal)

  putStrLn ("pascalRow 5    = " ++ show (pascalRow 5))

  putStrLn ("pascalAt 5 2   = " ++ show (pascalAt 5 2))

  putStrLn ("pascalAt 4 5   = " ++ show (pascalAt 4 5))

  putStrLn ("binomial 10 3  = " ++ show (binomial 10 3))

  putStrLn ("binomial 52 5  = " ++ show (binomial 52 5))

  putStrLn ("pascalAt 100 50 = " ++ show (pascalAt 100 50))
