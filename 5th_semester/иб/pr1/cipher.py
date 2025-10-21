import numpy as np


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

    def create_substitution_table_from_magic_square(self, magic_square: np.ndarray) -> dict:
        """Создание таблицы подстановки на основе магического квадрата"""
        chars = list(
            set(
                "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 .,!?-()[]{}:;'\""
            )
        )
        substituted = chars.copy()
        
        # Генерация seed из магического квадрата
        seed = self._generate_seed_from_magic_square(magic_square)
        np.random.seed(seed)
        np.random.shuffle(substituted)
        
        return dict(zip(chars, substituted))

    def _generate_seed_from_magic_square(self, magic_square: np.ndarray) -> int:
        """Генерация seed на основе магического квадрата"""
        n = magic_square.shape[0]
        
        # Сумма всех элементов
        total_sum = np.sum(magic_square)
        
        # Произведение диагоналей
        main_diag = np.diag(magic_square)
        anti_diag = np.diag(np.fliplr(magic_square))
        diag_product = np.prod(main_diag) * np.prod(anti_diag)
        
        # Комбинация особых элементов
        special_values = (
            magic_square[0, 0] * magic_square[n-1, n-1] +  # углы
            magic_square[n//2, n//2] +  # центр
            magic_square[0, n-1] * magic_square[n-1, 0]    # противоположные углы
        )
        
        # Комбинируем все методы
        final_seed = (total_sum + diag_product + special_values) & 0xFFFFFFFF
        
        return final_seed

    def apply_substitution(self, text: str, magic_square) -> str:
        """Применение подстановки к тексту"""
        sub_table = self.create_substitution_table_from_magic_square(magic_square)
        result = []

        for char in text:
            if char in sub_table:
                result.append(sub_table[char])
            else:
                result.append(char)

        return "".join(result)

    def reverse_substitution(self, text: str, magic_square) -> str:
        """Обратная подстановка"""
        sub_table = self.create_substitution_table_from_magic_square(magic_square)
        reverse_table = {v: k for k, v in sub_table.items()}
        result = []

        for char in text:
            if char in reverse_table:
                result.append(reverse_table[char])
            else:
                result.append(char)

        return "".join(result)

    def encrypt(self, plaintext: str, n: int, use_sub: bool) -> str:
        """Шифрование текста"""
        magic_square = self.generate_magic_square(n)

        # Применение подстановки (модификация)
        if use_sub:
            plaintext = self.apply_substitution(plaintext, magic_square)

        # Дополнение текста
        required_length = n * n
        if len(plaintext) < required_length:
            plaintext += self.padding_char * (required_length - len(plaintext))
        elif len(plaintext) > required_length:
            plaintext = plaintext[:required_length]

        # Генерация магического квадрата

        # Размещение символов в матрице
        text_matrix = np.array(list(plaintext)).reshape(n, n)

        # Чтение по значениям магического квадрата
        encrypted = [""] * (n * n)
        for i in range(n):
            for j in range(n):
                position = magic_square[i, j] - 1
                encrypted[position] = text_matrix[i, j]

        return "".join(encrypted)

    def decrypt(self, ciphertext: str, n: int, use_sub: bool) -> str:
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
        if use_sub:
            decrypted = self.reverse_substitution(decrypted, magic_square)

        return decrypted
