import numpy as np
import random
from typing import List, Tuple, Optional


class MagicSquareCipher:
    """Класс для шифрования на основе магических квадратов с поддержкой текстов любой длины"""

    def __init__(self):
        self.padding_char = "~"
        self.substitution_key = None

    def validate_magic_square(self, square: np.ndarray, check_uniqueness: bool = True) -> Tuple[bool, str]:
        """
        Проверка, является ли квадрат магическим
        
        Args:
            square: квадрат для проверки
            check_uniqueness: проверять ли уникальность чисел
            
        Returns:
            tuple: (is_valid: bool, message: str)
        """
        n = square.shape[0]
        
        if square.shape != (n, n):
            return False, f"Квадрат должен быть размером {n}x{n}"
        
        if check_uniqueness:
            all_numbers = square.flatten()
            if len(set(all_numbers)) != n * n:
                return False, "Все числа в квадрате должны быть уникальными"
        
        magic_sum = np.sum(square[0, :])
        
        # Проверка строк
        for i in range(n):
            if np.sum(square[i, :]) != magic_sum:
                return False, f"Строка {i+1} имеет неправильную сумму"
        
        # Проверка столбцов
        for j in range(n):
            if np.sum(square[:, j]) != magic_sum:
                return False, f"Столбец {j+1} имеет неправильную сумму"
        
        # Проверка диагоналей
        if np.sum(np.diag(square)) != magic_sum:
            return False, "Главная диагональ имеет неправильную сумму"
        
        if np.sum(np.diag(np.fliplr(square))) != magic_sum:
            return False, "Побочная диагональ имеет неправильную сумму"
        
        return True, f"Квадрат корректен! Магическая сумма: {magic_sum}"

    def generate_magic_square(self, n: int, method: str = "random", 
                            seed: Optional[int] = None, 
                            magic_sum: Optional[int] = None) -> np.ndarray:
        """
        Генерация магического квадрата разными методами
        Гарантирует возврат корректного магического квадрата
        """
        if seed is not None:
            np.random.seed(seed)
            random.seed(seed)
        
        max_attempts = 10
        for attempt in range(max_attempts):
            try:
                if method == "classic":
                    square = self._classic_magic_square(n)
                elif method == "random":
                    square = self._classic_with_safe_transformations(n)
                elif method == "arithmetic":
                    square = self._arithmetic_progression_square(n, magic_sum)
                elif method == "geometric":
                    square = self._modular_magic_square(n, magic_sum)
                else:
                    square = self._classic_magic_square(n)
                
                # Проверяем, что квадрат корректен
                is_valid, message = self.validate_magic_square(square)
                if is_valid:
                    return square
                    
            except Exception as e:
                continue
        
        # Если не удалось сгенерировать корректный квадрат, возвращаем классический
        return self._classic_magic_square(n)

    def _classic_with_safe_transformations(self, n: int) -> np.ndarray:
        """Классический квадрат с безопасными преобразованиями"""
        base = self._classic_magic_square(n)
        transformations = [self._rotate_square, self._reflect_square, self._transpose_square]
        
        result = base.copy()
        for _ in range(random.randint(2, 5)):
            result = random.choice(transformations)(result)
        
        return result

    def _ensure_encryption_range(self, square: np.ndarray) -> np.ndarray:
        """
        Гарантирует, что квадрат можно использовать для шифрования
        Преобразует квадрат так, чтобы числа были в диапазоне [1, n²] 
        и сохраняли магические свойства
        """
        n = square.shape[0]
        current_min = np.min(square)
        
        # Если числа уже в правильном диапазоне, возвращаем как есть
        if current_min >= 1 and np.max(square) <= n * n:
            # Проверяем уникальность
            if len(set(square.flatten())) == n * n:
                return square
        
        # Создаем новый классический квадрат и переносим магические свойства
        classic_square = self._classic_magic_square(n)
        
        # Используем относительный порядок чисел из исходного квадрата
        # чтобы создать перестановку классического квадрата
        flat_original = square.flatten()
        flat_classic = classic_square.flatten()
        
        # Сортируем индексы оригинального квадрата по значениям
        sorted_indices_original = np.argsort(flat_original)
        
        # Сортируем классический квадрат
        sorted_classic = np.sort(flat_classic)
        
        # Создаем mapping: позиция в отсортированном оригинале -> значение из классического
        result_flat = np.zeros(n * n, dtype=int)
        result_flat[sorted_indices_original] = sorted_classic
        
        return result_flat.reshape(n, n)

    def _classic_magic_square(self, n: int) -> np.ndarray:
        """Классический магический квадрат с числами 1..n²"""
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

    def _rotate_square(self, square: np.ndarray) -> np.ndarray:
        """Поворот квадрата"""
        angle = random.choice([1, 2, 3])
        return np.rot90(square, angle)

    def _reflect_square(self, square: np.ndarray) -> np.ndarray:
        """Отражение квадрата"""
        if random.choice([True, False]):
            return np.fliplr(square)
        else:
            return np.flipud(square)

    def _transpose_square(self, square: np.ndarray) -> np.ndarray:
        """Транспонирование квадрата - сохраняет магические свойства"""
        return square.T

    def _swap_symmetric_rows_columns(self, square: np.ndarray) -> np.ndarray:
        """Обмен симметричных строк и столбцов - ТОЛЬКО для квадратов с определенными свойствами"""
        n = square.shape[0]
        result = square.copy()
        
        # Этот метод работает только для некоторых типов магических квадратов
        if n % 2 == 1:  # только для нечетных размеров
            i = random.randint(0, n//2 - 1)
            j = n - 1 - i
            result[[i, j]] = result[[j, i]]
            result[:, [i, j]] = result[:, [j, i]]
        
        return result

    def _arithmetic_progression_square(self, n: int, magic_sum: Optional[int] = None) -> np.ndarray:
        """
        Арифметический магический квадрат
        """
        if magic_sum is None:
            magic_sum = n * (n * n + 1) // 2
        
        # Создаем классический квадрат и масштабируем
        base_square = self._classic_magic_square(n)
        base_sum = np.sum(base_square[0, :])
        
        if base_sum == 0:
            return base_square
        
        # Масштабируем к нужной сумме
        scale = magic_sum / base_sum
        result = (base_square * scale).astype(int)
        
        # Корректируем разницу
        current_sum = np.sum(result[0, :])
        diff = magic_sum - current_sum
        if diff != 0:
            result[0, 0] += diff
        
        return self._ensure_encryption_range(result)

    def _modular_magic_square(self, n: int, magic_sum: Optional[int] = None) -> np.ndarray:
        """
        Геометрический магический квадрат
        """
        # Для реального шифрования всегда используем классический квадрат
        # с преобразованием к нужной сумме
        return self._arithmetic_progression_square(n, magic_sum)

    def get_available_methods(self) -> List[str]:
        """Возвращает список доступных методов генерации"""
        return ["random", "classic", "arithmetic", "geometric"]

    def calculate_magic_sum(self, square: np.ndarray) -> int:
        """Вычисление магической суммы квадрата"""
        return int(np.sum(square[0, :]))

    def create_substitution_table_from_magic_square(self, magic_square: np.ndarray) -> dict:
        """Создание таблицы подстановки на основе магического квадрата"""
        chars = list(
            set(
                "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 .,!?-()[]{}:;'\""
            )
        )
        substituted = chars.copy()
        
        seed = self._generate_seed_from_magic_square(magic_square)
        np.random.seed(seed)
        np.random.shuffle(substituted)
        
        return dict(zip(chars, substituted))

    def _generate_seed_from_magic_square(self, magic_square: np.ndarray) -> int:
        """
        Генерация seed на основе магического квадрата без внешних зависимостей.
        Использует только свойства самого квадрата для детерминистической генерации.
        """
        n = magic_square.shape[0]
        
        # 1. Сумма всех элементов квадрата
        total_sum = np.sum(magic_square)
        
        # 2. Произведение элементов главной диагонали
        main_diag = np.diag(magic_square)
        main_diag_product = 1
        for num in main_diag:
            main_diag_product = (main_diag_product * (num if num != 0 else 1)) & 0xFFFFFFFF
        
        # 3. Произведение элементов побочной диагонали  
        anti_diag = np.diag(np.fliplr(magic_square))
        anti_diag_product = 1
        for num in anti_diag:
            anti_diag_product = (anti_diag_product * (num if num != 0 else 1)) & 0xFFFFFFFF
        
        # 4. Сумма угловых элементов
        corners_sum = (
            magic_square[0, 0] +      # левый верхний
            magic_square[0, n-1] +    # правый верхний
            magic_square[n-1, 0] +    # левый нижний
            magic_square[n-1, n-1]    # правый нижний
        )
        
        # 5. Центральный элемент (или сумма центральных для четных n)
        if n % 2 == 1:
            center_value = magic_square[n//2, n//2]
        else:
            center_value = (
                magic_square[n//2-1, n//2-1] +
                magic_square[n//2-1, n//2] +
                magic_square[n//2, n//2-1] +
                magic_square[n//2, n//2]
            )
        
        # 6. Характеристика распределения чисел - сумма модулей разностей соседних элементов
        neighbor_diff_sum = 0
        for i in range(n):
            for j in range(n-1):
                neighbor_diff_sum += abs(magic_square[i, j] - magic_square[i, j+1])
            if i < n-1:
                neighbor_diff_sum += abs(magic_square[i, 0] - magic_square[i+1, 0])
        
        # 7. Комбинируем все характеристики через битовые операции
        seed = total_sum
        
        # XOR с произведением диагоналей
        seed ^= main_diag_product
        seed ^= (anti_diag_product << 16) | (anti_diag_product >> 16)
        
        # Добавляем информацию об углах и центре
        seed = (seed + corners_sum * 0x9E3779B9) & 0xFFFFFFFF
        seed ^= (center_value * 0x85EBCA6B) & 0xFFFFFFFF
        
        # Добавляем информацию о распределении чисел
        seed = (seed + neighbor_diff_sum) & 0xFFFFFFFF
        seed = ((seed << 7) | (seed >> 25)) ^ 0xDEADBEEF
        
        # Финальное перемешивание
        seed = (seed * 0x343FD) & 0xFFFFFFFF
        seed = (seed + 0x269EC3) & 0xFFFFFFFF
        seed = seed ^ (seed >> 16)
        seed = (seed * 0x1B3) & 0xFFFFFFFF
        seed = seed ^ (seed >> 4)
        
        return seed & 0xFFFFFFFF

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

    def encrypt(self, plaintext: str, n: int, use_sub: bool, 
                method: str = "random", seed: Optional[int] = None,
                magic_sum: Optional[int] = None) -> str:
        """Шифрование текста любой длины с расширенной генерацией квадрата"""
        magic_square = self.generate_magic_square(n, method, seed, magic_sum)
        return self.encrypt_with_square(plaintext, magic_square, use_sub)

    def decrypt(self, ciphertext: str, n: int, use_sub: bool,
                method: str = "random", seed: Optional[int] = None,
                magic_sum: Optional[int] = None) -> str:
        """Расшифрование текста любой длины с расширенной генерацией квадрата"""
        magic_square = self.generate_magic_square(n, method, seed, magic_sum)
        return self.decrypt_with_square(ciphertext, magic_square, use_sub)

    def encrypt_with_square(self, plaintext: str, magic_square: np.ndarray, use_sub: bool) -> str:
        """Шифрование текста любой длины с использованием заданного квадрата"""
        n = magic_square.shape[0]
        block_size = n * n
        
        # Применение подстановки ко всему тексту
        if use_sub:
            plaintext = self.apply_substitution(plaintext, magic_square)
        
        # Разбиваем текст на блоки
        encrypted_blocks = []
        for i in range(0, len(plaintext), block_size):
            block = plaintext[i:i + block_size]
            
            # Дополнение последнего блока если нужно
            if len(block) < block_size:
                block += self.padding_char * (block_size - len(block))
            
            # Шифруем блок
            encrypted_block = self._encrypt_single_block(block, magic_square)
            encrypted_blocks.append(encrypted_block)
        
        return "".join(encrypted_blocks)

    def decrypt_with_square(self, ciphertext: str, magic_square: np.ndarray, use_sub: bool) -> str:
        """Расшифрование текста любой длины с использованием заданного квадрата"""
        n = magic_square.shape[0]
        block_size = n * n
        
        # Проверяем, что длина шифротекста кратна размеру блока
        if len(ciphertext) % block_size != 0:
            # Если нет, дополняем до кратности
            padding_needed = block_size - (len(ciphertext) % block_size)
            ciphertext += self.padding_char * padding_needed
        
        # Разбиваем шифротекст на блоки
        decrypted_blocks = []
        for i in range(0, len(ciphertext), block_size):
            block = ciphertext[i:i + block_size]
            
            # Расшифровываем блок
            decrypted_block = self._decrypt_single_block(block, magic_square)
            decrypted_blocks.append(decrypted_block)
        
        # Объединяем и удаляем дополнение
        result = "".join(decrypted_blocks)
        result = result.rstrip(self.padding_char)
        
        # Обратная подстановка
        if use_sub:
            result = self.reverse_substitution(result, magic_square)
        
        return result

    def _encrypt_single_block(self, block: str, magic_square: np.ndarray) -> str:
        """Шифрование одного блока текста"""
        n = magic_square.shape[0]
        
        # Проверяем, что блок правильного размера
        if len(block) != n * n:
            raise ValueError(f"Размер блока должен быть {n * n}, получен {len(block)}")
        
        # Размещение символов в матрице
        text_matrix = np.array(list(block)).reshape(n, n)
        
        # Чтение по значениям магического квадрата
        encrypted = [""] * (n * n)
        for i in range(n):
            for j in range(n):
                position = magic_square[i, j] - 1
                encrypted[position] = text_matrix[i, j]
        
        return "".join(encrypted)

    def _decrypt_single_block(self, block: str, magic_square: np.ndarray) -> str:
        """Расшифрование одного блока текста"""
        n = magic_square.shape[0]
        
        # Проверяем, что блок правильного размера
        if len(block) != n * n:
            raise ValueError(f"Размер блока должен быть {n * n}, получен {len(block)}")
        
        # Размещение символов по значениям магического квадрата
        decrypted_matrix = np.empty((n, n), dtype=str)
        
        for i in range(n):
            for j in range(n):
                position = magic_square[i, j] - 1
                decrypted_matrix[i, j] = block[position]
        
        # Чтение по порядку
        return "".join(decrypted_matrix.flatten())

    def get_block_size(self, magic_square: np.ndarray) -> int:
        """Возвращает размер блока для заданного квадрата"""
        n = magic_square.shape[0]
        return n * n

    def get_encryption_info(self, plaintext: str, magic_square: np.ndarray) -> dict:
        """Возвращает информацию о процессе шифрования"""
        n = magic_square.shape[0]
        block_size = n * n
        total_blocks = (len(plaintext) + block_size - 1) // block_size
        magic_sum = self.calculate_magic_sum(magic_square)
        
        return {
            "square_size": n,
            "block_size": block_size,
            "total_blocks": total_blocks,
            "magic_sum": magic_sum,
            "padding_char": self.padding_char
        }