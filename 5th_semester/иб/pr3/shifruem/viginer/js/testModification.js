// ----------------------------
// Алфавиты
// ----------------------------

// латиница (строчные и прописные)
const LATIN_LOWER = "abcdefghijklmnopqrstuvwxyz";
const LATIN_UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
// кириллица (строчные и прописные)
const CYRILLIC_LOWER = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя";
const CYRILLIC_UPPER = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ";

// общий алфавит (латиница + кириллица)
const ALPHABET = LATIN_LOWER + LATIN_UPPER + CYRILLIC_LOWER + CYRILLIC_UPPER;

// маппинг символ → индекс
function makeAlphabetMap(alphabet) {
  const map = {};
  for (let i = 0; i < alphabet.length; i++) {
    map[alphabet[i]] = i; // каждому символу ставим в соответствие индекс
  }
  return map;
}
const ALPHABET_MAP = makeAlphabetMap(ALPHABET);

// ----------------------------
// Генератор псевдослучайного потока байтов на основе HMAC-DRBG (SHA-256)
// ----------------------------
async function* hmacDrbgKeystream(seed) {  //Это асинхронный генератор, который бесконечно выдает псевдослучайные байты
  let counter = 1n;                           // счётчик, который будет инкрементироваться
  while (true) {
    const ctrBuf = new Uint8Array(8);         // каждый элемент массива - беззнаковое 8-битное целое число
    const view = new DataView(ctrBuf.buffer); // Теперь можно читать и записывать многобайтовые значения
    view.setBigUint64(0, counter);            // записываем в буфер текущее значение счётчика (BigInt)

    const key = await crypto.subtle.importKey(
      "raw",                                  // используем seed как «сырой» ключ
      seed,
      { name: "HMAC", hash: "SHA-256" },      // алгоритм: HMAC-SHA256
      /**
     * HMAC - алгоритм для вычисления кода аутентичности сообщений
     * SHA-256 - хеш-функция, которая будет использоваться внутри HMAC
     */

      false,                                  // нельзя извлечь ключ обратно в сыром виде
      ["sign"]                                // можно только подписывать (вычислять HMAC)
    );

    // подписываем (вычисляем HMAC) от счётчика с помощью ключа
    const mac = new Uint8Array(
      await crypto.subtle.sign("HMAC", key, ctrBuf)
    );

    yield mac;                                // отдаём блок (32 байта)
    counter++;                                // увеличиваем счётчик
  }
}

// Из генератора получаем ровно n байт
async function bytesFromHmacDrbg(seed, n) {
  const out = [];
  const gen = hmacDrbgKeystream(seed);        // берём поток блоков HMAC
  while (out.length < n) {
    const { value } = await gen.next();       // получаем очередной блок
    for (const b of value) {
      out.push(b);                            // накапливаем байты
      if (out.length >= n) break;
    }
  }
  return new Uint8Array(out);                 // возвращаем первые n байт
}

// ----------------------------
// Helpers
// ----------------------------

// Генератор равномерных чисел по модулю `modulus` из массива байтов
async function* uniformNumbersFromBytes(data, modulus) {
  /**
   * преобразует массив байтов (data) в последовательность псевдослучайных целых чисел в диапазоне от 0 до modulus - 1
   */
  let i = 0;
  while (i + 2 <= data.length) {
    const v = (data[i] << 8) | data[i + 1]; // читаем 16-битное число
                                        //Берутся два подряд идущих байта из массива.
                                        //Первый байт сдвигается на 8 бит влево (<< 8), второй добавляется как младший.
                                        //побитовое ИЛИ объединяет оба значения
                                        // Получается, как бы умножаем число на 2^8, и у нас образовывается 8 пустых разрядов(ноликов)
                                        // к ним как раз прибавляется разряды предыдущего бита
                                        // пример: 00001010 → 00001010 00000000 = data[i] , data[i]  + 00000001 = 00001010 00000001, где 00000001 - data[i + 1]
    i += 2;
    const limit = 65536 - (65536 % modulus);  // граница для отбраковки, чтобы числа равномерно распределялись
    if (v < limit) {
      yield v % modulus;                      // получаем число 0..modulus-1
    }
  }
}

// Получаем массив сдвигов (0..alphabetSize-1) для шифра Виженера
async function keystreamShifts(count, seed, alphabetSize) {
  /**
   * Назначение: Генерирует count случайных чисел 0..alphabetSize-1 из начального значения seed
   * Использование: Для создания ключевого потока в шифре Виженера
   */
  const shifts = [];
  const gen = hmacDrbgKeystream(seed);
  let buf = new Uint8Array(0);
  while (shifts.length < count) {
    const { value } = await gen.next();       // берём блок байтов
    const merged = new Uint8Array(buf.length + value.length); // создаём новый буфер, склеив старый и новый
    //  длина которого равна сумме старого буфера и новых данных.

    //typedArray.set(sourceArray, offset); Метод set() копирует данные из одного типизированного массива в другой.
    // offset - позиция, с которой начинается копирование
    merged.set(buf);                          // копируем старый буфер в начало
    merged.set(value, buf.length);            // добавляем новые байты в конец
    buf = merged;

    // из байтов получаем равномерные числа
    for await (const val of uniformNumbersFromBytes(buf, alphabetSize)) {
      shifts.push(val);
      if (shifts.length >= count) break;
    }
    if (buf.length > 2) buf = buf.slice(-1);  // оставляем «хвост» для корректной парности
  }
  return shifts;
}

// ----------------------------
// Шифр Виженера (универсальный)
// ----------------------------

// Шифрование текста: каждая буква сдвигается на значение из keystream
async function encryptVigenereText(plaintext, seed, alphabet = ALPHABET, alphabetMap = ALPHABET_MAP) {
  console.log(plaintext, seed)
  const letters = plaintext.split("").filter(ch => alphabetMap[ch] !== undefined).length;
  const shifts = await keystreamShifts(letters, seed, alphabet.length);

  let si = 0;
  const outChars = [];
  for (const ch of plaintext) {
    if (alphabetMap[ch] !== undefined) {      // символ из алфавита
      const shift = shifts[si++];
      const alphaIndex = alphabetMap[ch];
      const cipherIndex = (alphaIndex + shift) % alphabet.length; // сдвиг вперёд
      outChars.push(alphabet[cipherIndex]);
    } else {
      outChars.push(ch);                      // символы вне алфавита не трогаем
    }
  }
  return outChars.join("");
}

// Дешифрование текста: сдвиги вычитаются
async function decryptVigenereText(ciphertext, seed, alphabet = ALPHABET, alphabetMap = ALPHABET_MAP) {
  const letters = ciphertext.split("").filter(ch => alphabetMap[ch] !== undefined).length;
  const shifts = await keystreamShifts(letters, seed, alphabet.length);

  let si = 0;
  const outChars = [];
  for (const ch of ciphertext) {
    if (alphabetMap[ch] !== undefined) {
      const shift = shifts[si++];
      const alphaIndex = alphabetMap[ch];
      const plainIndex = (alphaIndex - shift + alphabet.length) % alphabet.length; // сдвиг назад
      outChars.push(alphabet[plainIndex]);
    } else {
      outChars.push(ch);
    }
  }
  return outChars.join("");
}

// ----------------------------
// Example usage
// ----------------------------
(async () => {
  const encoder = new TextEncoder();

  const pt = "Hello, мир! Смешанный текст: ABC xyz.";
  const seed = encoder.encode("Why are you so serious?"); // seed = ключ. Этот код кодирует строку в байты UTF-8.

  const ct = await encryptVigenereText(pt, seed, ALPHABET, ALPHABET_MAP);
  console.log("--- Text mode (latin + cyrillic) ---");
  console.log("Plain:", pt);
  console.log("Cipher:", ct);

  const recovered = await decryptVigenereText(ct, seed, ALPHABET, ALPHABET_MAP);
  console.log("Recovered:", recovered);
})();

export default { encryptVigenereText, decryptVigenereText };
