function vigenereCipher(text, key, encrypt = false) {
    // Определяем алфавит
    const alphabet = 'АБВГДЕЁЖЗИЙКЛМНОРСТУФХЦЧШЩПЪЫЬЭЮЯ';

    // Функция для проверки типа символа
    function isLetter(char) {
        return /[А-ЯЁ]/i.test(char);
    }

    // Подготовка ключа
    let preparedKey = '';
    let keyIndex = 0;

    // Создаем ключ той же длины, что и текст
    for (let i = 0; i < text.length; i++) {
        if (isLetter(text[i])) {
            // Берем следующий символ ключа
            let currentKeyChar;

            currentKeyChar = key[keyIndex % key.length];
            keyIndex++;

            preparedKey += currentKeyChar

        } else {
            preparedKey += text[i]; // Неалфавитные символы оставляем как есть
            keyIndex++; // Продвигаем индекс ключа для синхронизации
        }
    }

    let result = '';

    for (let i = 0; i < text.length; i++) {
        const char = text[i];
        const keyChar = preparedKey[i];

        // Пропускаем неалфавитные символы
        if (!isLetter(char)) {
            result += char;
            continue;
        }

        const isUpperCase = char === char.toUpperCase();

        // Находим индексы символов
        const charIndex = alphabet.indexOf(char.toUpperCase());
        const keyCharIndex = alphabet.indexOf(keyChar.toUpperCase());

        if (charIndex === -1 || keyCharIndex === -1) {
            result += char;
            continue;
        }

        let newIndex;
        if (encrypt) {
            // Шифрование
            newIndex = (charIndex + keyCharIndex) % alphabet.length;
        } else {
            // Дешифрование
            newIndex = (charIndex - keyCharIndex + alphabet.length) % alphabet.length;
        }

        // Сохраняем регистр
        result += isUpperCase ? alphabet[newIndex] : alphabet[newIndex].toLowerCase();
    }

    return result;
}

export default vigenereCipher