
groupConsecutive :: Eq a => [a] -> [[a]]
groupConsecutive [] = []
groupConsecutive (x:xs) = (x : takeWhile' x xs) : groupConsecutive (dropWhile' x xs)
  where
    -- берём элементы, пока они равны y
    takeWhile' _ [] = []
    takeWhile' y (z:zs)
      | y == z    = z : takeWhile' y zs
      | otherwise = []
    -- отбрасываем элементы, пока они равны y
    dropWhile' _ [] = []
    dropWhile' y (z:zs)
      | y == z    = dropWhile' y zs
      | otherwise = z : zs


minPositive :: [Int] -> Maybe Int
minPositive [] = Nothing
minPositive (x:xs)
  | x > 0     = case minPositive xs of
                   Nothing -> Just x
                   Just m  -> if x < m then Just x else Just m
  | otherwise  = minPositive xs
