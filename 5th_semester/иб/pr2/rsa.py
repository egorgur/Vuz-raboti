import random
import math
import os
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
        """Вычисление размера блока для данных с учетом PKCS#1 дополнения"""
        n_bits = self.n.bit_length()
        k = (n_bits + 7) // 8  # Размер модуля в байтах
        return max(1, k - 11)  # PKCS#1 overhead

    def _pad_block_pkcs1_v1_5(self, data: bytes) -> int:
        """
        Дополнение блока по схеме PKCS#1 v1.5 для шифрования
        
        Формат: 0x00 || 0x02 || [случайные ненулевые байты] || 0x00 || [данные]
        """
        k = (self.n.bit_length() + 7) // 8  # Размер модуля в байтах
        data_len = len(data)
        
        if data_len > k - 11:
            raise ValueError(f"Data too long for PKCS#1 padding. Max: {k-11} bytes, got: {data_len} bytes")
        
        # Вычисляем длину случайных байтов
        padding_len = k - data_len - 3  # -3 для 0x00, 0x02, 0x00
        
        if padding_len < 8:
            raise ValueError("Insufficient space for PKCS#1 padding (need at least 8 random bytes)")
        
        # Генерируем случайные ненулевые байты
        random_bytes = bytearray()
        while len(random_bytes) < padding_len:
            random_byte = os.urandom(1)[0]
            if random_byte != 0:
                random_bytes.append(random_byte)
        
        # Собираем полный блок
        padded_block = b'\x00\x02' + bytes(random_bytes) + b'\x00' + data
        
        # Конвертируем в число для шифрования
        return int.from_bytes(padded_block, byteorder='big')

    def _unpad_block_pkcs1_v1_5(self, block_int: int) -> bytes:
        """
        Удаление дополнения PKCS#1 v1.5 после дешифрования
        """
        k = (self.n.bit_length() + 7) // 8
        block_bytes = block_int.to_bytes(k, byteorder='big')
        
        # Проверяем формат блока
        if block_bytes[0] != 0x00:
            raise ValueError("Invalid PKCS#1 padding: first byte must be 0x00")
        
        if block_bytes[1] != 0x02:
            raise ValueError("Invalid PKCS#1 padding: second byte must be 0x02")
        
        # Ищем разделитель 0x00
        separator_index = -1
        for i in range(2, len(block_bytes)):
            if block_bytes[i] == 0x00:
                separator_index = i
                break
        
        if separator_index == -1:
            raise ValueError("Invalid PKCS#1 padding: separator 0x00 not found")
        
        # Проверяем, что случайных байтов достаточно (минимум 8)
        random_bytes_count = separator_index - 2
        if random_bytes_count < 8:
            raise ValueError("Invalid PKCS#1 padding: insufficient random bytes")
        
        # Извлекаем данные после разделителя
        data = block_bytes[separator_index + 1:]
        
        return data

    def _text_to_blocks(self, text: str) -> List[int]:
        """Преобразование текста в числовые блоки с PKCS#1 дополнением"""
        # Кодируем текст в UTF-8
        text_bytes = text.encode("utf-8")
        block_size = self._calculate_block_size()

        blocks = []

        # Разбиваем на блоки и применяем дополнение
        for i in range(0, len(text_bytes), block_size):
            block_data = text_bytes[i:i + block_size]
            padded_block = self._pad_block_pkcs1_v1_5(block_data)
            blocks.append(padded_block)

        return blocks

    def _blocks_to_text(self, blocks: List[int]) -> str:
        """Преобразование числовых блоков обратно в текст с удалением дополнения"""
        bytes_list = bytearray()

        for block in blocks:
            # Удаляем дополнение PKCS#1
            try:
                block_data = self._unpad_block_pkcs1_v1_5(block)
                bytes_list.extend(block_data)
            except ValueError as e:
                raise ValueError(f"Failed to unpad block: {e}")

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
        n_bits = self.n.bit_length()
        k_bytes = (n_bits + 7) // 8
        
        return {
            "p": self.p,
            "q": self.q,
            "n": self.n,
            "n_bits": n_bits,
            "n_bytes": k_bytes,
            "phi": self.phi,
            "public_exponent": self.e,
            "private_exponent": self.d,
            "n_digits": len(str(self.n)),
            "block_size_bytes": self._calculate_block_size(),
            "max_data_per_block": f"{self._calculate_block_size()} bytes",
            "security_level": "LOW" if n_bits < 1024 else "MEDIUM" if n_bits < 2048 else "HIGH"
        }