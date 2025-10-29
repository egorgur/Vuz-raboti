import random
import math
from typing import Tuple, List


class RSAEncryption:
    def __init__(self, n_digits: int = 31):
        self.n_digits = n_digits
        self.p, self.q = self._generate_primes()
        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)
        self.e = self._choose_public_exponent()
        self.d = self._calculate_private_key()

    def _is_prime(self, num: int) -> bool:
        """Проверка числа на простоту"""
        if num < 2:
            return False
        if num == 2:
            return True
        if num % 2 == 0:
            return False

        # Упрощенная проверка для демонстрации
        limit = int(math.isqrt(num)) + 1
        for i in range(3, limit, 2):
            if num % i == 0:
                return False
        return True

    def _generate_primes(self) -> Tuple[int, int]:
        """Генерация двух простых чисел P и Q"""
        # Для N с 31 цифрами, P и Q должны быть примерно по 15-16 цифр
        p_digits = self.n_digits // 2
        q_digits = self.n_digits - p_digits

        p_min = 10 ** (p_digits - 1)
        p_max = 10**p_digits - 1

        q_min = 10 ** (q_digits - 1)
        q_max = 10**q_digits - 1

        # Генерируем P
        while True:
            p = random.randint(p_min, p_max)
            if self._is_prime(p):
                break

        # Генерируем Q
        while True:
            q = random.randint(q_min, q_max)
            if self._is_prime(q) and p != q:
                n = p * q
                if len(str(n)) == self.n_digits:
                    break

        return p, q

    def _gcd(self, a: int, b: int) -> int:
        """Наибольший общий делитель"""
        while b:
            a, b = b, a % b
        return a

    def _choose_public_exponent(self) -> int:
        """Выбор открытой экспоненты e"""
        # Стандартные значения e
        for e in [65537, 257, 17, 3]:
            if 1 < e < self.phi and self._gcd(e, self.phi) == 1:
                return e

        # Если стандартные не подходят, ищем случайное
        while True:
            e = random.randint(3, self.phi - 1)
            if self._gcd(e, self.phi) == 1:
                return e

    def _extended_gcd(self, a: int, b: int) -> Tuple[int, int, int]:
        """Расширенный алгоритм Евклида"""
        if a == 0:
            return b, 0, 1

        gcd, x1, y1 = self._extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

    def _calculate_private_key(self) -> int:
        """Вычисление закрытого ключа d"""
        _, x, _ = self._extended_gcd(self.e, self.phi)
        d = x % self.phi
        if d < 0:
            d += self.phi
        return d

    def _calculate_block_size(self) -> int:
        """Вычисление размера блока в байтах"""
        # Блок должен быть меньше N
        n_bits = self.n.bit_length()
        # Оставляем запас для безопасного кодирования
        block_size_bytes = (n_bits - 1) // 8
        return max(1, block_size_bytes)

    def _text_to_blocks(self, text: str) -> List[int]:
        """Преобразование текста в числовые блоки"""
        # Кодируем текст в UTF-8
        text_bytes = text.encode("utf-8")
        block_size = self._calculate_block_size()

        blocks = []

        # Разбиваем на блоки
        for i in range(0, len(text_bytes), block_size):
            block_bytes = text_bytes[i : i + block_size]
            # Преобразуем байты в число
            block_int = 0
            for byte in block_bytes:
                block_int = (block_int << 8) | byte
            blocks.append(block_int)

        return blocks

    def _blocks_to_text(self, blocks: List[int]) -> str:
        """Преобразование числовых блоков обратно в текст"""
        bytes_list = bytearray()
        block_size = self._calculate_block_size()

        for block in blocks:
            # Извлекаем байты из блока
            block_bytes = bytearray()
            temp_block = block

            # Извлекаем байты в правильном порядке
            for _ in range(block_size):
                if temp_block == 0:
                    break
                byte = temp_block & 0xFF
                block_bytes.append(byte)
                temp_block >>= 8

            # Байты извлекаются в обратном порядке
            block_bytes.reverse()
            bytes_list.extend(block_bytes)

        # Удаляем возможные нулевые байты в конце
        while bytes_list and bytes_list[-1] == 0:
            bytes_list.pop()

        return bytes_list.decode("utf-8", errors="replace")

    def _modular_pow(self, base: int, exponent: int, modulus: int) -> int:
        """Быстрое возведение в степень по модулю"""
        result = 1
        base = base % modulus

        while exponent > 0:
            if exponent & 1:
                result = (result * base) % modulus
            exponent = exponent >> 1
            base = (base * base) % modulus

        return result

    def encrypt(self, plaintext: str) -> Tuple[List[int], dict]:
        """Шифрование текста"""
        if not plaintext:
            return [], {}

        blocks = self._text_to_blocks(plaintext)
        encrypted_blocks = [
            self._modular_pow(block, self.e, self.n) for block in blocks
        ]

        public_key = {"e": self.e, "n": self.n}

        return encrypted_blocks, public_key

    def decrypt(self, encrypted_blocks: List[int]) -> str:
        """Дешифрование текста"""
        if not encrypted_blocks:
            return ""

        decrypted_blocks = [
            self._modular_pow(block, self.d, self.n) for block in encrypted_blocks
        ]
        return self._blocks_to_text(decrypted_blocks)

    def get_key_info(self) -> dict:
        """Информация о ключах"""
        return {
            "p": self.p,
            "q": self.q,
            "n": self.n,
            "phi": self.phi,
            "public_exponent": self.e,
            "private_exponent": self.d,
            "n_digits": len(str(self.n)),
            "block_size_bytes": self._calculate_block_size(),
        }
