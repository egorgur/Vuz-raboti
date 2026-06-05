module Main where

import System.CPUTime (getCPUTime)
import System.IO (BufferMode (NoBuffering), hSetBuffering, isEOF, stdout)
import Text.Read (readMaybe)

generateSecret :: IO Int
generateSecret = do
  t <- getCPUTime
  return (fromInteger (t `mod` 100) + 1)

-- readGuess - безопасное чтение числа с проверкой диапазона 1..100

readGuess :: IO (Either String Int)
readGuess = do
  line <- getLine
  case readMaybe line :: Maybe Int of
    Nothing ->
      return (Left ("это не целое число: " ++ show line))
    Just n
      | n < 1 || n > 100 ->
          return (Left ("число вне диапазона 1..100: " ++ show n))
      | otherwise ->
          return (Right n)

-- playRound - один раунд: спрашиваем число, пока не угадано или не EOF

playRound :: Int -> Int -> IO ()
playRound secret attempts = do
  putStr "Ваш вариант (1..100): "
  eof <- isEOF
  if eof
    then putStrLn "\nВвод завершён (EOF). До встречи!"
    else do
      result <- readGuess

      case result of
        Left err -> do
          putStrLn ("Ошибка: " ++ err)
          playRound secret attempts
        Right guess ->
          let attempts' = attempts + 1
           in case compare guess secret of
                LT -> do
                  putStrLn "Загаданное число больше."
                  playRound secret attempts'
                GT -> do
                  putStrLn "Загаданное число меньше."
                  playRound secret attempts'
                EQ ->
                  putStrLn ("Поздравляю! Вы угадали за " ++ show attempts' ++ " попыток.")

gameLoop :: IO ()
gameLoop = do
  secret <- generateSecret
  putStrLn "Я загадал число от 1 до 100. Угадывайте!"
  playRound secret 0
  putStr "Сыграть ещё раз? (y/n): "
  eof <- isEOF
  if eof
    then putStrLn "\nЗавершение игры."
    else do
      answer <- getLine

      if answer `elem` ["y", "Y", "д", "Д", "yes", "да"]
        then gameLoop
        else putStrLn "Спасибо за игру!"

main :: IO ()
main = do
  hSetBuffering stdout NoBuffering
  putStrLn "=== Игра «Угадай число» ==="

  gameLoop
