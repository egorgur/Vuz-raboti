module Main where

import Data.Ratio (denominator, numerator)
import GHC.Real qualified
import Prelude hiding (Rational)

data Rational = R Int Int

-- reduce - сокращение дроби на НОД и нормализация знака (знаменатель > 0)

reduce :: Rational -> Rational
reduce (R n d) = R (n * s `div` g) (d * s `div` g)
  where
    s = signum d
    g = gcd n d

-- add - сложение: a/b + c/d = (a*d + c*b) / (b*d)

add :: Rational -> Rational -> Rational
add (R a b) (R c d) = reduce (R (a * d + c * b) (b * d))

-- multiply - умножение: a/b * c/d = (a*c) / (b*d)

multiply :: Rational -> Rational -> Rational
multiply (R a b) (R c d) = reduce (R (a * c) (b * d))

-- toDouble - преобразование рационального числа в Double

toDouble :: Rational -> Double
toDouble (R a b) = fromIntegral a / fromIntegral b

-- instance Num Rational — арифметика через add, multiply, negate

instance Num Rational where
  (+) :: Rational -> Rational -> Rational
  (+) = add

  (*) :: Rational -> Rational -> Rational
  (*) = multiply

  negate :: Rational -> Rational
  negate (R a b) = R (negate a) b

  abs :: Rational -> Rational
  abs (R a b) = R (abs a) (abs b)

  signum :: Rational -> Rational
  signum (R a b) = R (signum a * signum b) 1

  fromInteger :: Integer -> Rational
  fromInteger n = R (fromInteger n) 1

-- instance Fractional Rational — деление: a/b / c/d = (a*d) / (b*c)

instance Fractional Rational where
  (/) :: Rational -> Rational -> Rational
  (R a b) / (R c d) = reduce (R (a * d) (b * c))

  fromRational :: GHC.Real.Rational -> Rational
  fromRational q = reduce (R (fromInteger (numerator q)) (fromInteger (denominator q)))

-- instance Eq Rational — равенство через сокращение

instance Eq Rational where
  (==) :: Rational -> Rational -> Bool
  r1 == r2 = a == c && b == d
    where
      R a b = reduce r1
      R c d = reduce r2

-- instance Ord Rational — порядок через кросс-умножение

instance Ord Rational where
  compare :: Rational -> Rational -> Ordering
  compare r1 r2 = compare (a * d) (c * b)
    where
      R a b = reduce r1
      R c d = reduce r2

-- instance Show Rational — красивый вывод (добавлен для удобства тестирования)

instance Show Rational where
  show :: Rational -> String
  show r = case reduce r of
    R a 1 -> show a
    R a b -> show a ++ "/" ++ show b

main :: IO ()
main = do
  let z1 = R 3 4

  let z2 = R 1 (-2)

  let z3 = R 6 8

  putStrLn ("z1 = " ++ show z1)
  putStrLn ("z2 = " ++ show z2)

  putStrLn ("reduce (6/8) = " ++ show (reduce z3))

  putStrLn ("z1 + z2 = " ++ show (z1 + z2))

  putStrLn ("z1 * z2 = " ++ show (z1 * z2))

  putStrLn ("negate z1 = " ++ show (negate z1))

  putStrLn ("z1 / z2 = " ++ show (z1 / z2))

  putStrLn ("toDouble z1 = " ++ show (toDouble z1))

  putStrLn ("z1 == reduce z3 ? " ++ show (z1 == reduce z3))

  putStrLn ("z2 < z1 ? " ++ show (z2 < z1))

  putStrLn ("compare z1 z2 = " ++ show (compare z1 z2))
