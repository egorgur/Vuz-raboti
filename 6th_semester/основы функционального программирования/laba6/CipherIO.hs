module CipherIO
  ( processFile,
    readFileSafe,
    writeFileSafe,
  )
where

import Cipher (CipherMode (..), validateKey, vigenereDecrypt, vigenereEncrypt)
import Control.Exception (IOException, catch)

handleIO :: String -> IOException -> IO (Either String a)
handleIO action e = return (Left (action ++ " failed: " ++ show e))

-- Безопасное чтение файла

readFileSafe :: FilePath -> IO (Either String String)
readFileSafe path =
  (Right <$> readFile path) `catch` handleIO ("Reading " ++ path)

-- Безопасная запись файла

writeFileSafe :: FilePath -> String -> IO (Either String ())
writeFileSafe path contents =
  (Right <$> writeFile path contents) `catch` handleIO ("Writing " ++ path)

processFile :: CipherMode -> String -> FilePath -> FilePath -> IO (Either String ())
processFile mode key inPath outPath =
  case validateKey key of
    Left err -> return (Left err)
    Right () -> do
      readResult <- readFileSafe inPath

      case readResult of
        Left err -> return (Left err)
        Right contents -> do
          let transformed = case mode of
                Encrypt -> vigenereEncrypt key contents
                Decrypt -> vigenereDecrypt key contents
          writeFileSafe outPath transformed

