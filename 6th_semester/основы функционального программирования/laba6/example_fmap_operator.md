# Пример оператора `<$>` в Haskell

`<$>` — это инфиксная форма функции `fmap`.

```haskell
f <$> x
```

означает:

```haskell
fmap f x
```

То есть функция `f` применяется не к самому контейнеру, а к значению **внутри** контейнера.

---

## Пример с `Maybe`

```haskell
(+1) <$> Just 5
```

Результат:

```haskell
Just 6
```

А если значения нет:

```haskell
(+1) <$> Nothing
```

Результат:

```haskell
Nothing
```

---

## Пример со списком

```haskell
(*2) <$> [1, 2, 3]
```

Результат:

```haskell
[2, 4, 6]
```

Это то же самое, что:

```haskell
map (*2) [1, 2, 3]
```

---

## Пример из `CipherIO.hs`

В файле используется строка:

```haskell
Right <$> readFile path
```

Разберём типы:

```haskell
readFile path :: IO String
Right         :: String -> Either String String
```

`readFile path` читает файл и возвращает результат внутри `IO`.

`<$>` применяет `Right` к строке, которая находится внутри `IO`.

Поэтому:

```haskell
Right <$> readFile path
```

имеет тип:

```haskell
IO (Either String String)
```

То есть успешное чтение файла превращается в:

```haskell
Right contents
```

но всё это остаётся внутри `IO`.

---

## То же самое без `<$>`

Запись:

```haskell
Right <$> readFile path
```

можно переписать так:

```haskell
do
  contents <- readFile path
  return (Right contents)
```

Обе версии делают одно и то же.

---

## В контексте обработки ошибок

В `CipherIO.hs` полная строка такая:

```haskell
(Right <$> readFile path) `catch` handleIO ("Reading " ++ path)
```

Смысл:

1. Попробовать прочитать файл.
2. Если получилось — вернуть `Right contents`.
3. Если произошла ошибка чтения — `catch` перехватит её и вернёт `Left error`.

Итоговый тип функции:

```haskell
readFileSafe :: FilePath -> IO (Either String String)
```

То есть результат такой:

- `Right contents` — файл успешно прочитан;
- `Left error` — произошла ошибка.
