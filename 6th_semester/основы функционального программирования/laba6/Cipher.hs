module Cipher
  ( CipherMode (..),
    vigenereEncrypt,
    vigenereDecrypt,
    substitutionEncrypt,
    substitutionDecrypt,
    invertTable,
    makeTable,
    validateKey,
  )
where

import Data.Char (chr, isAsciiLower, isAsciiUpper, ord)
import Data.Maybe (fromMaybe)

-- Тип режима шифрования (АТД-«перечисление»)

data CipherMode = Encrypt | Decrypt
  deriving (Eq, Show)

isAsciiLetter :: Char -> Bool
isAsciiLetter c = isAsciiUpper c || isAsciiLower c

keyShift :: Char -> Int
keyShift c
  | isAsciiUpper c = ord c - ord 'A'
  | isAsciiLower c = ord c - ord 'a'
  | otherwise = 0

shiftChar :: Int -> Char -> Char
shiftChar n c
  | isAsciiUpper c = chr ((ord c - ord 'A' + n) `mod` 26 + ord 'A')
  | isAsciiLower c = chr ((ord c - ord 'a' + n) `mod` 26 + ord 'a')
  | otherwise = c

vigenereCipher :: Int -> String -> String -> String
vigenereCipher sign key text
  | null shifts = text
  | otherwise = go (cycle shifts) text
  where
    shifts = map keyShift (filter isAsciiLetter key)
    go _ [] = []
    go (k : rest) (c : cs)
      | isAsciiLetter c = shiftChar (sign * k) c : go rest cs
      | otherwise = c : go (k : rest) cs
    go [] cs = cs

-- берёт список сдвигов ключа
-- берёт текст
-- идёт по тексту посимвольно
-- если символ — буква, шифрует его и переходит к следующему сдвигу
-- если символ — пробел/цифра/знак, оставляет его как есть и не тратит букву ключа

-- Публичные функции Виженера

vigenereEncrypt :: String -> String -> String
vigenereEncrypt = vigenereCipher 1

vigenereDecrypt :: String -> String -> String
vigenereDecrypt = vigenereCipher (-1)

-- Шифр подстановки

substitutionEncrypt :: [(Char, Char)] -> String -> String


substitutionEncrypt table = map (\c -> fromMaybe c (lookup c table))

-- `map (\c -> ...)` применяет лямбду к каждому символу.
--   `lookup c table :: Maybe Char` ищет замену для `c`; `fromMaybe c` берёт
--   найденную замену либо оставляет `c`, если замены нет.
--   Лямбда `\c -> ...` — анонимная функция; `\` вводит параметр.
--   Зачем map + lookup + fromMaybe: декларативно «заменить каждый символ по
--   таблице, неизвестные — без изменений».

invertTable :: [(Char, Char)] -> [(Char, Char)]
-- Обращение таблицы: меняем местами «откуда» и «куда».

invertTable = map (\(a, b) -> (b, a))

-- Лямбда с образцом-кортежем `\(a, b) -> (b, a)` распаковывает пару и
--   переставляет элементы. Зачем: дешифрование подстановки = шифрование по
--   обратной таблице.

substitutionDecrypt :: [(Char, Char)] -> String -> String
substitutionDecrypt table = substitutionEncrypt (invertTable table)

-- Дешифрование = подстановка по обращённой таблице. Переиспользуем уже
--   написанную логику — типичный приём «выразить одно через другое».

-- -----------------------------------------------------------------------------
-- Построение таблицы и валидация (граничные проверки чистой логики)
-- -----------------------------------------------------------------------------

makeTable :: String -> String -> Either String [(Char, Char)]
-- Из двух алфавитов («откуда» и «куда») строим таблицу или сообщаем об ошибке.
--   `Either String [(Char,Char)]` — либо ошибка-строка, либо готовая таблица.

makeTable from to
  | length from /= length to =
      Left "Substitution alphabets must have equal length"
  -- Guard: при несовпадении длин (`/=` — «не равно») возвращаем Left с причиной.
  --   Зачем: обработка граничного случая «несовпадение длин при подстановке».
  | otherwise = Right (zip from to)

-- `zip from to` попарно соединяет символы в список пар — это и есть таблица.
--   Заворачиваем в Right как успешный результат.

validateKey :: String -> Either String ()
-- Валидация ключа Виженера. Результат — `Either String ()`: при успехе
--   полезного значения нет (`()`), важен лишь факт «ок/ошибка».

validateKey key
  | null key = Left "Key must not be empty"
  -- `null` проверяет пустоту списка/строки.
  | all isAsciiLetter key = Right ()
  -- `all p xs` — истинно, если предикат `p` выполнен для ВСЕХ элементов.
  --   Здесь: все символы ключа — латинские буквы.
  | otherwise = Left "Key must contain only letters"

-- Иначе сообщаем, что ключ содержит недопустимые символы.
--   Зачем Either, а не Maybe: нужно вернуть ТЕКСТ причины ошибки, а не просто
--   признак неудачи — это требование «детализированных ошибок» бизнес-логики.
