import Prelude hiding (zipWith3)

groupConsec :: Eq a => [a] -> [[a]]
groupConsec = foldr step []
  where
    step x []                    = [[x]]
    step x ((y:ys):gs)
      | x == y    = (x : y : ys) : gs
      | otherwise = [x] : ((y:ys):gs)    
    step x ([] : gs)             = [x] : gs

groupLengths :: Eq a => [a] -> [Int]
groupLengths = map length . groupConsec




zipWith3 :: (a -> b -> c -> d) -> [a] -> [b] -> [c] -> [d]
zipWith3 f xs ys = zipWith ($) (zipWith f xs ys)

