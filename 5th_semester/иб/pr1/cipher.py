import numpy as np
import hashlib


class MagicSquareCipher:
    """Класс для шифрования на основе магических квадратов"""

    def __init__(self):
        self.padding_char = "~"
        self.substitution_key = None

    def generate_magic_square(self, n: int) -> np.ndarray:
        """Генерация магического квадрата размером n x n"""
        if n % 2 == 1:
            return self._odd_magic_square(n)
        elif n % 4 == 0:
            return self._doubly_even_magic_square(n)
        else:
            return self._singly_even_magic_square(n)

    def _odd_magic_square(self, n: int) -> np.ndarray:
        """Генерация магического квадрата для нечетного n"""
        magic_square = np.zeros((n, n), dtype=int)
        i, j = 0, n // 2

        for num in range(1, n * n + 1):
            magic_square[i, j] = num
            new_i, new_j = (i - 1) % n, (j + 1) % n

            if magic_square[new_i, new_j] != 0:
                i = (i + 1) % n
            else:
                i, j = new_i, new_j

        return magic_square

    def _doubly_even_magic_square(self, n: int) -> np.ndarray:
        """Генерация магического квадрата для n кратного 4"""
        magic_square = np.arange(1, n * n + 1).reshape(n, n)

        for i in range(0, n, 4):
            for j in range(0, n, 4):
                for k in range(4):
                    magic_square[i + k, j + k] = n * n + 1 - magic_square[i + k, j + k]
                    magic_square[i + k, j + 3 - k] = (
                        n * n + 1 - magic_square[i + k, j + 3 - k]
                    )

        return magic_square

    def _singly_even_magic_square(self, n: int) -> np.ndarray:
        """Генерация магического квадрата для n = 4k + 2"""
        size = n // 2
        magic_square = np.zeros((n, n), dtype=int)

        sub_square = self._odd_magic_square(size)

        # Заполнение квадрантов
        magic_square[:size, :size] = sub_square
        magic_square[size:, size:] = sub_square + size * size
        magic_square[:size, size:] = sub_square + 2 * size * size
        magic_square[size:, :size] = sub_square + 3 * size * size

        # Корректировка для магического квадрата
        k = (n - 2) // 4

        for i in range(size):
            for j in range(k):
                if i == size // 2:
                    j_swap = j + k
                else:
                    j_swap = j

                magic_square[i, j_swap], magic_square[i + size, j_swap] = (
                    magic_square[i + size, j_swap],
                    magic_square[i, j_swap],
                )

        for i in range(size):
            for j in range(k - 1):
                magic_square[i, n - j - 1], magic_square[i + size, n - j - 1] = (
                    magic_square[i + size, n - j - 1],
                    magic_square[i, n - j - 1],
                )

        return magic_square

    def create_substitution_table(self, key: str) -> dict:
        """Создание таблицы подстановки на основе ключа"""
        hash_obj = hashlib.sha256(key.encode())
        hash_hex = hash_obj.hexdigest()

        chars = list(
            set(
                "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 .,!?-()[]{}:;'\""
            )
        )
        substituted = chars.copy()

        # Перемешивание на основе хеша
        seed = int(hash_hex[:8], 16)
        np.random.seed(seed)
        np.random.shuffle(substituted)

        return dict(zip(chars, substituted))

    def apply_substitution(self, text: str, key: str) -> str:
        """Применение подстановки к тексту"""
        if not key:
            return text

        sub_table = self.create_substitution_table(key)
        result = []

        for char in text:
            if char in sub_table:
                result.append(sub_table[char])
            else:
                result.append(char)

        return "".join(result)

    def reverse_substitution(self, text: str, key: str) -> str:
        """Обратная подстановка"""
        if not key:
            return text

        sub_table = self.create_substitution_table(key)
        reverse_table = {v: k for k, v in sub_table.items()}
        result = []

        for char in text:
            if char in reverse_table:
                result.append(reverse_table[char])
            else:
                result.append(char)

        return "".join(result)

    def encrypt(self, plaintext: str, n: int, substitution_key: str = "") -> str:
        """Шифрование текста"""
        # Применение подстановки (модификация)
        if substitution_key:
            plaintext = self.apply_substitution(plaintext, substitution_key)

        # Дополнение текста
        required_length = n * n
        if len(plaintext) < required_length:
            plaintext += self.padding_char * (required_length - len(plaintext))
        elif len(plaintext) > required_length:
            plaintext = plaintext[:required_length]

        # Генерация магического квадрата
        magic_square = self.generate_magic_square(n)

        # Размещение символов в матрице
        text_matrix = np.array(list(plaintext)).reshape(n, n)

        # Чтение по значениям магического квадрата
        encrypted = [""] * (n * n)
        for i in range(n):
            for j in range(n):
                position = magic_square[i, j] - 1
                encrypted[position] = text_matrix[i, j]

        return "".join(encrypted)

    def decrypt(self, ciphertext: str, n: int, substitution_key: str = "") -> str:
        """Расшифрование текста"""
        if len(ciphertext) != n * n:
            raise ValueError(f"Длина шифротекста должна быть {n * n}")

        # Генерация магического квадрата
        magic_square = self.generate_magic_square(n)

        # Размещение символов по значениям магического квадрата
        decrypted_matrix = np.empty((n, n), dtype=str)

        for i in range(n):
            for j in range(n):
                position = magic_square[i, j] - 1
                decrypted_matrix[i, j] = ciphertext[position]

        # Чтение по порядку
        decrypted = "".join(decrypted_matrix.flatten())

        # Удаление дополнительных символов
        decrypted = decrypted.rstrip(self.padding_char)

        # Обратная подстановка (модификация)
        if substitution_key:
            decrypted = self.reverse_substitution(decrypted, substitution_key)

        return decrypted
