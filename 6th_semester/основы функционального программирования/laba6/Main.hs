-- =============================================================================
-- Main.hs — Практическая работа №6, Вариант 7. Модуль ИНТЕРФЕЙСА.
-- =============================================================================
-- Слой взаимодействия с пользователем: меню, ввод параметров, вызов чистой
-- логики (Cipher) и граничных функций (CipherIO), вывод результатов/ошибок.
-- Сборка проекта: ghc --make Main.hs -o cipher   (соберёт все три модуля)
-- =============================================================================

module Main where
-- Модуль Main с функцией main — точка входа исполняемой программы.

import System.IO (hSetBuffering, BufferMode(NoBuffering), stdout, isEOF)
-- Средства ввода-вывода: управление буферизацией и проверка конца ввода `isEOF`.
--   `BufferMode(NoBuffering)` импортирует тип вместе с нужным конструктором.
--   Зачем: приглашения должны появляться сразу, а Ctrl+D — не ронять программу.

import Cipher
-- Импорт ВСЕГО экспортируемого из модуля чистой логики (без списка имён).
--   Зачем без списка: интерфейсу нужны почти все функции шифрования и типы.

import CipherIO (processFile)
-- Из граничного модуля берём только processFile (файловая операция Виженера).

-- -----------------------------------------------------------------------------
-- Сценарий Виженера: ключ + файлы (демонстрирует processFile, Either+IO)
-- -----------------------------------------------------------------------------

runVigenere :: CipherMode -> IO ()
-- Принимает режим (Encrypt/Decrypt), ничего полезного не возвращает (IO ()).

runVigenere mode = do
  putStr "Key (letters only): "
-- `putStr` — приглашение без перевода строки.
  key <- getLine
-- Считываем ключ с консоли в `key :: String`.
  case validateKey key of
-- Проверяем ключ ЧИСТОЙ функцией из Cipher; `case` разбирает Either.
    Left err -> putStrLn ("Key error: " ++ err)
-- Ключ плох — печатаем причину и выходим из сценария (граничный случай).
    Right () -> do
      putStr "Input file:  "
      inPath  <- getLine
-- Путь входного файла.
      putStr "Output file: "
      outPath <- getLine
-- Путь выходного файла.
      result <- processFile mode key inPath outPath
-- Вызов граничной функции; `result :: Either String ()`.
      case result of
        Left err -> putStrLn ("Error: " ++ err)
-- Ошибка файла/чтения/записи — сообщаем пользователю.
        Right () -> putStrLn ("Done. Result written to " ++ outPath)
-- Успех — подтверждаем запись.

-- -----------------------------------------------------------------------------
-- Сценарий подстановки: два алфавита + текст (демонстрирует makeTable, границы)
-- -----------------------------------------------------------------------------

runSubstitution :: CipherMode -> IO ()
runSubstitution mode = do
  putStr "Alphabet FROM: "
  fromA <- getLine
-- Алфавит-источник (какие символы заменяем).
  putStr "Alphabet TO:   "
  toA   <- getLine
-- Алфавит-назначение (на что заменяем).
  case makeTable fromA toA of
-- Строим таблицу ЧИСТОЙ функцией; при разной длине вернётся Left (граничный случай).
    Left err -> putStrLn ("Table error: " ++ err)
    Right table -> do
      let table' = if mode == Encrypt then table else invertTable table
-- `if ... then ... else ...` выбирает прямую или обращённую таблицу.
--   `mode == Encrypt` использует выведённый Eq для CipherMode.
--   Зачем invertTable при Decrypt: дешифрование подстановки = замена по
--   обратной таблице.
      putStr "Text: "
      text <- getLine
      putStrLn ("Result: " ++ substitutionEncrypt table' text)
-- Применяем подстановку (для дешифрования table' уже обращена) и печатаем.

-- -----------------------------------------------------------------------------
-- Интерактивное меню
-- -----------------------------------------------------------------------------

menuLoop :: IO ()
menuLoop = do
  putStrLn ""
  putStrLn "=== Cipher menu ==="
  putStrLn "1. Vigenere encrypt (file)"
  putStrLn "2. Vigenere decrypt (file)"
  putStrLn "3. Substitution encrypt (text)"
  putStrLn "4. Substitution decrypt (text)"
  putStrLn "5. Exit"
  putStr   "Choose: "
  eof <- isEOF
-- Проверяем EOF перед чтением, чтобы Ctrl+D завершал программу аккуратно.
  if eof
    then putStrLn "\nBye."
    else do
      choice <- getLine
      case choice of
-- Разбор выбора пользователя по строке. `>>` последовательно выполняет два
--   IO-действия, игнорируя результат первого: «сделать сценарий, затем меню снова».
        "1" -> runVigenere Encrypt          >> menuLoop
        "2" -> runVigenere Decrypt          >> menuLoop
        "3" -> runSubstitution Encrypt      >> menuLoop
        "4" -> runSubstitution Decrypt      >> menuLoop
        "5" -> putStrLn "Bye."
-- Выход: не вызываем menuLoop, рекурсия прекращается.
        _   -> putStrLn "Invalid choice." >> menuLoop
-- Образец `_` ловит любой другой ввод (граничный случай неверного пункта).

-- -----------------------------------------------------------------------------
-- main — точка входа
-- -----------------------------------------------------------------------------

main :: IO ()
main = do
  hSetBuffering stdout NoBuffering
-- Отключаем буферизацию вывода, чтобы приглашения (`putStr` без `\n`)
--   показывались до ввода пользователя.
  putStrLn "=== Vigenere / Substitution cipher ==="
  menuLoop
-- Запускаем цикл меню; вся работа происходит внутри него.
