# Объяснение кода: Шифратор/дешифратор (ПР №6, Вариант 7)

Проект разбит на три модуля по слоям ответственности:

| Модуль | Слой | Назначение |
|--------|------|-----------|
| `Cipher` | Чистая логика | Алгоритмы шифрования и валидация. Никакого ввода-вывода. Ошибки — через `Either`. |
| `CipherIO` | Граница с ОС | Чтение/запись файлов, перехват системных исключений. Тип `IO (Either ...)`. |
| `Main` | Интерфейс | Меню, диалог с пользователем, связывание логики и границы. |

Зависимости направлены строго «вниз»: `Main → CipherIO → Cipher`. Чистая логика не знает ни о файлах, ни о консоли, поэтому её легко тестировать и переиспользовать.

---

## Модуль `Cipher` — чистая логика

### Тип режима

```haskell
data CipherMode = Encrypt | Decrypt
  deriving (Eq, Show)
```

`CipherMode` — алгебраический тип-перечисление (сумма типов) с двумя конструкторами без полей. Он используется вместо строки или булева флага, чтобы компилятор гарантировал: режим может быть **только** `Encrypt` или `Decrypt`. Опечатка вроде `"encrupt"` стала бы невозможной. `deriving (Eq, Show)` автоматически даёт возможность сравнивать (`mode == Encrypt`) и печатать значение.

### Работа с буквами

Три приватные (неэкспортируемые) функции инкапсулируют арифметику над символами:

- `isAsciiLetter` — предикат «латинская буква» (заглавная или строчная). Ограничение ASCII важно: алгоритм сдвигает только A–Z/a–z, а пробелы, цифры и не-ASCII символы оставляет нетронутыми.
- `keyShift` — превращает букву ключа в число сдвига `0..25` (A/a → 0, B/b → 1, …). Регистр учитывается отдельной базой отсчёта (`ord 'A'` или `ord 'a'`).
- `shiftChar` — сдвигает букву на `n` позиций по кольцу алфавита, сохраняя регистр:

```haskell
shiftChar n c
  | isAsciiUpper c = chr ((ord c - ord 'A' + n) `mod` 26 + ord 'A')
  | isAsciiLower c = chr ((ord c - ord 'a' + n) `mod` 26 + ord 'a')
  | otherwise      = c
```

Ключевая деталь — `` `mod` 26``. Алфавит цикличен: после `Z` снова идёт `A`. Поскольку в Haskell `mod` при положительном делителе всегда возвращает неотрицательный остаток, отрицательный сдвиг при дешифровании (например `-10`) корректно «заворачивается» в диапазон `0..25` без отдельной обработки.

### Шифр Виженера

Обе операции выражены через одну общую функцию, параметризованную знаком сдвига:

```haskell
vigenereCipher :: Int -> String -> String -> String
vigenereCipher sign key text
  | null shifts = text
  | otherwise   = go (cycle shifts) text
  where
    shifts = map keyShift (filter isAsciiLetter key)
    go _ [] = []
    go (k:rest) (c:cs)
      | isAsciiLetter c = shiftChar (sign * k) c : go rest cs
      | otherwise       = c : go (k:rest) cs
    go [] cs = cs
```

Что здесь происходит:

1. `filter isAsciiLetter key` оставляет в ключе только буквы, `map keyShift` переводит их в числовые сдвиги. Это классическая комбинация `map`/`filter`.
2. `cycle shifts` создаёт **бесконечный** циклический список сдвигов. Ключ обычно короче текста и должен повторяться. Благодаря **ленивости** этот бесконечный список вычисляется ровно настолько, насколько нужно по длине текста — отдельная логика «возврата к началу ключа» не требуется.
3. Рекурсивная `go` идёт по тексту посимвольно. Для буквы она берёт текущий сдвиг `k` и **продвигает** ключ (`rest`); для не-буквы оставляет символ и **не продвигает** ключ (`k:rest`). Так ключ синхронизируется только с буквами — это поведение настоящего шифра Виженера.
4. `null shifts` защищает от `cycle []` (бесконечного зацикливания на пустом ключе), оставляя функцию тотальной даже без внешней валидации.

Публичные обёртки фиксируют знак в point-free стиле:

```haskell
vigenereEncrypt = vigenereCipher 1     -- сдвиг вперёд
vigenereDecrypt = vigenereCipher (-1)  -- сдвиг назад
```

Аргументы `key` и `text` здесь не пишутся явно — они «дотекают» сами (частичное применение). Скобки в `(-1)` обязательны, иначе это читалось бы как вычитание.

**Пример:** ключ `KEY`, текст `HELLO` → `RIJVS`; обратно `RIJVS` с тем же ключом → `HELLO`.

### Шифр подстановки

```haskell
substitutionEncrypt table = map (\c -> fromMaybe c (lookup c table))
invertTable               = map (\(a, b) -> (b, a))
substitutionDecrypt table = substitutionEncrypt (invertTable table)
```

Таблица — это ассоциативный список пар `[(Char, Char)]`. Для каждого символа `lookup c table` ищет замену (`Maybe Char`), а `fromMaybe c` берёт найденную замену либо оставляет символ как есть, если его нет в таблице. Дешифрование выражено через шифрование по **обращённой** таблице — пример переиспользования логики вместо дублирования.

### Валидация и построение таблицы

```haskell
validateKey key
  | null key              = Left "Key must not be empty"
  | all isAsciiLetter key = Right ()
  | otherwise             = Left "Key must contain only letters"

makeTable from to
  | length from /= length to = Left "Substitution alphabets must have equal length"
  | otherwise                = Right (zip from to)
```

Обе функции возвращают `Either String x`: в `Left` — **текст** причины ошибки, в `Right` — успешный результат. Здесь выбран `Either`, а не `Maybe`, именно потому, что нужно сообщить пользователю *что именно* не так. `validateKey` возвращает `Right ()`, так как при успехе важен лишь факт корректности, а не какое-то значение. `makeTable` обрабатывает граничный случай «несовпадение длин алфавитов».

---

## Модуль `CipherIO` — граничные функции

Здесь сосредоточен весь ввод-вывод и перехват системных исключений. Тип результата `IO (Either String a)` совмещает два смысла: `IO` — это эффект (обращение к файловой системе), а внутренний `Either` — бизнес-результат (успех или ошибка с причиной).

### Перехват исключений

```haskell
handleIO :: String -> IOException -> IO (Either String a)
handleIO action e = return (Left (action ++ " failed: " ++ show e))
```

Системные сбои (файла нет, нет прав на запись) приходят как исключения типа `IOException`. Единый обработчик `handleIO` превращает такое исключение в аккуратное `Left "..."`, чтобы программа не падала. Конкретный тип `IOException` во втором аргументе подсказывает функции `catch`, исключения какого класса перехватывать.

### Безопасные чтение и запись

```haskell
readFileSafe path =
  (Right <$> readFile path) `catch` handleIO ("Reading " ++ path)

writeFileSafe path contents =
  (Right <$> writeFile path contents) `catch` handleIO ("Writing " ++ path)
```

Оператор `<$>` (это `fmap`) применяет `Right` **внутри** `IO`, превращая, например, `IO String` в `IO (Either String String)`. Конструкция `действие `catch` обработчик` означает: выполнить действие, а при исключении передать его в `handleIO`, который вернёт `Left`. Так любая файловая операция либо даёт `Right`-результат, либо `Left` с описанием.

### Основная операция

```haskell
processFile mode key inPath outPath =
  case validateKey key of
    Left err -> return (Left err)
    Right () -> do
      readResult <- readFileSafe inPath
      case readResult of
        Left err       -> return (Left err)
        Right contents -> do
          let transformed = case mode of
                              Encrypt -> vigenereEncrypt key contents
                              Decrypt -> vigenereDecrypt key contents
          writeFileSafe outPath transformed
```

Логика выстроена как последовательность «шлюзов»:

1. Сначала **чистая** проверка ключа (`validateKey`) — если плохой, файлы вообще не трогаются.
2. Затем безопасное чтение; ошибка чтения сразу пробрасывается в `Left`.
3. **Чистое** преобразование (`let transformed = …`) — здесь IO не нужен, только вычисление. Внутренний `case mode of` выбирает шифрование или дешифрование.
4. Безопасная запись; её результат `IO (Either String ())` и есть итог всей функции, поэтому отдельный `return` не нужен.

Это наглядная демонстрация принципа: эффекты (чтение/запись) изолированы по краям, а в середине — чистое вычисление.

---

## Модуль `Main` — интерфейс

Слой взаимодействия с пользователем. Он собирает параметры, вызывает логику и границу, печатает результат.

### Сценарий Виженера

```haskell
runVigenere mode = do
  putStr "Key (letters only): "
  key <- getLine
  case validateKey key of
    Left err -> putStrLn ("Key error: " ++ err)
    Right () -> do
      putStr "Input file:  "
      inPath  <- getLine
      putStr "Output file: "
      outPath <- getLine
      result <- processFile mode key inPath outPath
      case result of
        Left err -> putStrLn ("Error: " ++ err)
        Right () -> putStrLn ("Done. Result written to " ++ outPath)
```

`do`-нотация выполняет IO-действия по порядку; `<-` извлекает результат действия (например, введённую строку). Каждый `Either` разбирается через `case`: ветка `Left` печатает причину ошибки, ветка `Right` продолжает работу. Здесь видно разделение ролей: проверка ключа — чистая (`validateKey`), а файловая работа — граничная (`processFile`).

### Сценарий подстановки

```haskell
runSubstitution mode = do
  ...
  case makeTable fromA toA of
    Left err -> putStrLn ("Table error: " ++ err)
    Right table -> do
      let table' = if mode == Encrypt then table else invertTable table
      putStr "Text: "
      text <- getLine
      putStrLn ("Result: " ++ substitutionEncrypt table' text)
```

`makeTable` строит таблицу или возвращает ошибку при разной длине алфавитов. Для дешифрования таблица обращается (`invertTable`), а сама замена всегда идёт через `substitutionEncrypt`. Сравнение `mode == Encrypt` работает благодаря выведённому `Eq` у `CipherMode`.

### Меню

```haskell
menuLoop = do
  ...
  eof <- isEOF
  if eof
    then putStrLn "\nBye."
    else do
      choice <- getLine
      case choice of
        "1" -> runVigenere Encrypt     >> menuLoop
        "2" -> runVigenere Decrypt     >> menuLoop
        "3" -> runSubstitution Encrypt >> menuLoop
        "4" -> runSubstitution Decrypt >> menuLoop
        "5" -> putStrLn "Bye."
        _   -> putStrLn "Invalid choice." >> menuLoop
```

Цикл реализован рекурсией: каждый пункт делает свой сценарий и вызывает `menuLoop` снова через `>>` (последовательное выполнение двух IO-действий с игнорированием результата первого). Пункт `5` просто не вызывает `menuLoop`, и рекурсия прекращается. Образец `_` ловит любой неверный ввод. Проверка `isEOF` перед чтением обеспечивает корректное завершение по Ctrl+D вместо аварии `getLine`.

В `main` дополнительно вызывается `hSetBuffering stdout NoBuffering`, чтобы приглашения (`putStr` без перевода строки) появлялись на экране сразу, до ввода пользователя.

---

## Поток данных (на примере шифрования файла)

```
Main.runVigenere (IO: ввод ключа и путей)
        │
        ▼
Cipher.validateKey            -- чистая проверка → Either
        │ Right ()
        ▼
CipherIO.processFile
        ├── CipherIO.readFileSafe   -- IO + Either (перехват исключений)
        │        │ Right contents
        │        ▼
        ├── Cipher.vigenereEncrypt  -- ЧИСТОЕ преобразование
        │        │
        │        ▼
        └── CipherIO.writeFileSafe  -- IO + Either
                 │
                 ▼
        Either String ()  →  обратно в меню (печать результата)
```

---

## Использованные паттерны ФП

- **Алгебраические типы данных:** `CipherMode` исключает некорректные состояния на уровне типов.
- **`Either` для ошибок, `IO` для эффектов:** бизнес-ошибки несут текст причины; внешние эффекты явно отделены типом `IO`.
- **Разделение чистого и эффектного:** алгоритмы (`Cipher`) не содержат IO; эффекты живут только в `CipherIO` и `Main`.
- **Функции высшего порядка и лямбды:** `map`, `filter`, анонимные функции в подстановке.
- **Point-free стиль:** `vigenereEncrypt = vigenereCipher 1`.
- **Ленивость:** бесконечный `cycle` ключа берётся ровно по длине текста.
- **Рекурсия и сопоставление с образцом:** обход текста в `vigenereCipher`, цикл меню в `menuLoop`.

## Сборка и запуск

```bash
ghc --make Main.hs -o cipher   # компиляция всех трёх модулей
./cipher                       # запуск
# либо без компиляции:
runghc Main.hs
```

## Анализ сложности

При длине текста `n`, размере таблицы подстановки `m` и длине ключа `k`:

- Виженер — `O(n)`: каждый символ обрабатывается один раз.
- Подстановка — `O(n · m)` из-за `lookup` по ассоциативному списку (ускоряется до `O(n · log m)` на `Data.Map`).
- `validateKey`, `makeTable` — `O(k)`.
