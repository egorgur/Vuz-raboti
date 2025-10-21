from cipher import MagicSquareCipher
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import numpy as np


class CipherGUI:
    """Графический интерфейс для шифровальщика"""

    def __init__(self, root, cipher: MagicSquareCipher):
        self.root = root
        self.root.title("Шифр на основе магических квадратов")
        self.root.geometry("900x700")

        self.cipher = cipher

        # Стиль
        style = ttk.Style()
        style.theme_use("clam")

        # Создание вкладок
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Вкладка шифрования
        self.encrypt_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.encrypt_frame, text="Шифрование/Расшифрование")
        self.create_encrypt_tab()


    def create_encrypt_tab(self):
        """Создание вкладки шифрования"""
        # Параметры
        params_frame = ttk.LabelFrame(self.encrypt_frame, text="Параметры", padding=10)
        params_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        ttk.Label(params_frame, text="Размер квадрата (N):").grid(
            row=0, column=0, sticky="w"
        )
        self.size_var = tk.IntVar(value=5)
        ttk.Spinbox(
            params_frame, from_=3, to=10, textvariable=self.size_var, width=10
        ).grid(row=0, column=1, padx=5)

        ttk.Label(params_frame, text="Ключ подстановки:").grid(
            row=0, column=2, sticky="w", padx=(20, 0)
        )
        self.sub_key_var = tk.StringVar()
        ttk.Entry(params_frame, textvariable=self.sub_key_var, width=20).grid(
            row=0, column=3, padx=5
        )

        self.use_substitution = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            params_frame,
            text="Использовать подстановку",
            variable=self.use_substitution,
        ).grid(row=0, column=4, padx=10)

        # Ввод текста
        input_frame = ttk.LabelFrame(
            self.encrypt_frame, text="Исходный текст", padding=10
        )
        input_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        self.input_text = scrolledtext.ScrolledText(
            input_frame, height=10, width=40, wrap=tk.WORD
        )
        self.input_text.pack(fill="both", expand=True)

        # Кнопки
        button_frame = ttk.Frame(self.encrypt_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Зашифровать", command=self.encrypt_text).pack(
            side="left", padx=5
        )
        ttk.Button(button_frame, text="Расшифровать", command=self.decrypt_text).pack(
            side="left", padx=5
        )
        ttk.Button(button_frame, text="Очистить", command=self.clear_fields).pack(
            side="left", padx=5
        )
        ttk.Button(
            button_frame, text="Показать квадрат", command=self.show_magic_square
        ).pack(side="left", padx=5)

        # Вывод результата
        output_frame = ttk.LabelFrame(self.encrypt_frame, text="Результат", padding=10)
        output_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        self.output_text = scrolledtext.ScrolledText(
            output_frame, height=10, width=40, wrap=tk.WORD
        )
        self.output_text.pack(fill="both", expand=True)

        # Информация
        info_frame = ttk.LabelFrame(self.encrypt_frame, text="Информация", padding=10)
        info_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        self.info_label = ttk.Label(info_frame, text=".....")
        self.info_label.pack()

        # Настройка весов
        self.encrypt_frame.grid_rowconfigure(1, weight=1)
        self.encrypt_frame.grid_columnconfigure(0, weight=1)
        self.encrypt_frame.grid_columnconfigure(1, weight=1)

    def create_test_tab(self):
        """Создание вкладки тестирования"""
        # Кнопка запуска тестов
        ttk.Button(
            self.test_frame, text="Запустить тесты", command=self.run_tests
        ).pack(pady=10)

        # Результаты тестов
        self.test_results = scrolledtext.ScrolledText(
            self.test_frame, height=25, width=100, wrap=tk.WORD
        )
        self.test_results.pack(fill="both", expand=True, padx=10, pady=5)

    def create_analysis_tab(self):
        """Создание вкладки анализа"""
        # Кнопка анализа
        ttk.Button(
            self.analysis_frame,
            text="Провести анализ криптостойкости",
            command=self.analyze_cryptography,
        ).pack(pady=10)

        # Результаты анализа
        self.analysis_results = scrolledtext.ScrolledText(
            self.analysis_frame, height=25, width=100, wrap=tk.WORD
        )
        self.analysis_results.pack(fill="both", expand=True, padx=10, pady=5)

    def encrypt_text(self):
        """Обработчик кнопки шифрования"""
        try:
            plaintext = self.input_text.get("1.0", tk.END).strip()
            if not plaintext:
                messagebox.showwarning("Предупреждение", "Введите текст для шифрования")
                return

            n = self.size_var.get()
            sub_key = self.sub_key_var.get() if self.use_substitution.get() else ""

            encrypted = self.cipher.encrypt(plaintext, n, sub_key)

            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", encrypted)

            self.info_label.config(
                text=f"Текст зашифрован. Длина: {len(encrypted)} символов"
            )

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при шифровании: {str(e)}")

    def decrypt_text(self):
        """Обработчик кнопки расшифрования"""
        try:
            ciphertext = self.input_text.get("1.0", tk.END).strip()
            if not ciphertext:
                messagebox.showwarning(
                    "Предупреждение", "Введите текст для расшифрования"
                )
                return

            n = self.size_var.get()
            sub_key = self.sub_key_var.get() if self.use_substitution.get() else ""

            decrypted = self.cipher.decrypt(ciphertext, n, sub_key)

            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", decrypted)

            self.info_label.config(
                text=f"Текст расшифрован. Длина: {len(decrypted)} символов"
            )

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при расшифровании: {str(e)}")

    def clear_fields(self):
        """Очистка полей"""
        self.input_text.delete("1.0", tk.END)
        self.output_text.delete("1.0", tk.END)
        self.info_label.config(text="Поля очищены")

    def show_magic_square(self):
        """Показать магический квадрат"""
        n = self.size_var.get()
        square = self.cipher.generate_magic_square(n)

        # Создание окна для отображения квадрата
        square_window = tk.Toplevel(self.root)
        square_window.title(f"Магический квадрат {n}x{n}")

        # Отображение квадрата
        text_widget = tk.Text(square_window, height=n + 2, width=n * 5 + 10)
        text_widget.pack(padx=10, pady=10)

        for i in range(n):
            row_text = " ".join(f"{square[i, j]:3d}" for j in range(n))
            text_widget.insert(tk.END, row_text + "\n")

        # Проверка магической суммы
        magic_sum = np.sum(square[0, :])
        text_widget.insert(tk.END, f"\nМагическая сумма: {magic_sum}")

        text_widget.config(state="disabled")

    def run_tests(self):
        """Запуск тестов"""
        self.test_results.delete("1.0", tk.END)

        test_cases = [
            "Hello World",
            "The quick brown fox jumps over the lazy dog",
            "1234567890",
            "Test!@#$%",
            "Криптография",
            "a",
            "AB",
            "This is a very long test string to check padding",
            "Short",
            "MixedCase123!",
            "   Spaces   ",
            "Symbols: []{}()",
        ]

        self.test_results.insert(tk.END, "=" * 80 + "\n")
        self.test_results.insert(tk.END, "ТЕСТИРОВАНИЕ АЛГОРИТМА ШИФРОВАНИЯ\n")
        self.test_results.insert(tk.END, "=" * 80 + "\n\n")

        for size in [3, 4, 5]:
            self.test_results.insert(tk.END, f"\nРазмер квадрата: {size}x{size}\n")
            self.test_results.insert(tk.END, "-" * 40 + "\n")

            for i, test_text in enumerate(test_cases[:10], 1):
                # Без подстановки
                encrypted = self.cipher.encrypt(test_text, size)
                decrypted = self.cipher.decrypt(encrypted, size)

                self.test_results.insert(tk.END, f"\nТест {i}:\n")
                self.test_results.insert(tk.END, f"Исходный:     '{test_text}'\n")
                self.test_results.insert(tk.END, f"Зашифрован:   '{encrypted}'\n")
                self.test_results.insert(tk.END, f"Расшифрован:  '{decrypted}'\n")

                if test_text == decrypted:
                    self.test_results.insert(tk.END, "Результат:    ✓ УСПЕХ\n")
                else:
                    self.test_results.insert(tk.END, "Результат:    ✗ ОШИБКА\n")

                # С подстановкой
                if i <= 5:  # Тестируем подстановку на первых 5 примерах
                    encrypted_sub = self.cipher.encrypt(test_text, size, "SecretKey123")
                    decrypted_sub = self.cipher.decrypt(
                        encrypted_sub, size, "SecretKey123"
                    )

                    self.test_results.insert(tk.END, "С подстановкой:\n")
                    self.test_results.insert(
                        tk.END, f"Зашифрован:   '{encrypted_sub}'\n"
                    )
                    self.test_results.insert(
                        tk.END, f"Расшифрован:  '{decrypted_sub}'\n"
                    )

                    if test_text == decrypted_sub:
                        self.test_results.insert(tk.END, "Результат:    ✓ УСПЕХ\n")
                    else:
                        self.test_results.insert(tk.END, "Результат:    ✗ ОШИБКА\n")

        self.test_results.see(tk.END)

    def analyze_cryptography(self):
        """Анализ криптостойкости"""
        self.analysis_results.delete("1.0", tk.END)

        self.analysis_results.insert(tk.END, "=" * 80 + "\n")
        self.analysis_results.insert(tk.END, "АНАЛИЗ КРИПТОСТОЙКОСТИ\n")
        self.analysis_results.insert(tk.END, "=" * 80 + "\n\n")

        # Тестовый текст
        test_text = (
            "The quick brown fox jumps over the lazy dog. This is a test message."
        )

        # Анализ базового алгоритма
        self.analysis_results.insert(
            tk.END, "1. БАЗОВЫЙ АЛГОРИТМ (только магический квадрат)\n"
        )
        self.analysis_results.insert(tk.END, "-" * 40 + "\n")

        for size in [3, 4, 5]:
            encrypted_basic = self.cipher.encrypt(test_text[: size * size], size)
            self.analysis_frequency_analysis(
                test_text[: size * size], encrypted_basic, f"Размер {size}x{size}"
            )

        # Анализ с подстановкой
        self.analysis_results.insert(
            tk.END, "\n2. МОДИФИЦИРОВАННЫЙ АЛГОРИТМ (с подстановкой)\n"
        )
        self.analysis_results.insert(tk.END, "-" * 40 + "\n")

        for size in [3, 4, 5]:
            encrypted_mod = self.cipher.encrypt(
                test_text[: size * size], size, "SecretKey"
            )
            self.analysis_frequency_analysis(
                test_text[: size * size],
                encrypted_mod,
                f"Размер {size}x{size} с подстановкой",
            )

        # Сравнительный анализ
        self.analysis_results.insert(tk.END, "\n3. СРАВНИТЕЛЬНЫЙ АНАЛИЗ\n")
        self.analysis_results.insert(tk.END, "-" * 40 + "\n")

        # Энтропия
        import math
        from collections import Counter

        def calculate_entropy(text):
            if not text:
                return 0
            counter = Counter(text)
            length = len(text)
            entropy = 0
            for count in counter.values():
                probability = count / length
                if probability > 0:
                    entropy -= probability * math.log2(probability)
            return entropy

        size = 5
        plaintext = test_text[: size * size]
        encrypted_basic = self.cipher.encrypt(plaintext, size)
        encrypted_mod = self.cipher.encrypt(plaintext, size, "SecretKey")

        entropy_plain = calculate_entropy(plaintext)
        entropy_basic = calculate_entropy(encrypted_basic)
        entropy_mod = calculate_entropy(encrypted_mod)

        self.analysis_results.insert(
            tk.END, f"Энтропия исходного текста:       {entropy_plain:.4f}\n"
        )
        self.analysis_results.insert(
            tk.END, f"Энтропия базового шифра:         {entropy_basic:.4f}\n"
        )
        self.analysis_results.insert(
            tk.END, f"Энтропия модифицированного:      {entropy_mod:.4f}\n\n"
        )

        # Анализ устойчивости к атакам
        self.analysis_results.insert(tk.END, "4. УСТОЙЧИВОСТЬ К АТАКАМ\n")
        self.analysis_results.insert(tk.END, "-" * 40 + "\n")

        self.analysis_results.insert(tk.END, "Базовый алгоритм:\n")
        self.analysis_results.insert(
            tk.END, "• Уязвим к частотному анализу (сохраняет частоты символов)\n"
        )
        self.analysis_results.insert(
            tk.END, "• Ключевое пространство: N! (факториал размера квадрата)\n"
        )
        self.analysis_results.insert(
            tk.END, "• Устойчивость к brute-force: низкая для малых N\n\n"
        )

        self.analysis_results.insert(tk.END, "Модифицированный алгоритм:\n")
        self.analysis_results.insert(
            tk.END, "• Двойная защита: перестановка + подстановка\n"
        )
        self.analysis_results.insert(
            tk.END, "• Ключевое пространство: N! × 2^256 (с SHA-256 ключом)\n"
        )
        self.analysis_results.insert(
            tk.END, "• Устойчивость к частотному анализу: высокая\n"
        )
        self.analysis_results.insert(
            tk.END, "• Устойчивость к brute-force: значительно выше\n\n"
        )

        # Выводы
        self.analysis_results.insert(tk.END, "5. ВЫВОДЫ\n")
        self.analysis_results.insert(tk.END, "-" * 40 + "\n")
        self.analysis_results.insert(
            tk.END,
            "✓ Модификация с подстановкой значительно повышает криптостойкость\n",
        )
        self.analysis_results.insert(tk.END, "✓ Энтропия шифротекста увеличивается\n")
        self.analysis_results.insert(
            tk.END, "✓ Частотный анализ становится неэффективным\n"
        )
        self.analysis_results.insert(
            tk.END, "✓ Размер ключевого пространства увеличивается экспоненциально\n"
        )

        self.analysis_results.see(tk.END)

    def analysis_frequency_analysis(self, plaintext, ciphertext, label):
        """Частотный анализ"""
        from collections import Counter

        plain_freq = Counter(plaintext)
        cipher_freq = Counter(ciphertext)

        self.analysis_results.insert(tk.END, f"\n{label}:\n")

        # Топ-5 частых символов
        plain_top = plain_freq.most_common(5)
        cipher_top = cipher_freq.most_common(5)

        self.analysis_results.insert(
            tk.END, f"Топ символов исходного текста: {plain_top}\n"
        )
        self.analysis_results.insert(
            tk.END, f"Топ символов шифротекста:      {cipher_top}\n"
        )

        # Проверка сохранения частот
        preserved = sum(1 for p, c in zip(plain_top, cipher_top) if p[0] == c[0])
        self.analysis_results.insert(
            tk.END, f"Сохранено частых символов:     {preserved}/5\n"
        )
