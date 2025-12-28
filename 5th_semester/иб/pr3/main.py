import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox


class VigenereCracker:
    def __init__(self):
        # Русский алфавит (33 буквы) - ДОБАВЛЕНА БУКВА Ё
        self.alphabet = ""
        self.alphabet_ё = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
        self.alphabet_e = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
        self.alphabet_size = len(self.alphabet)  # Теперь 33

        self.russian_freq = []

        # Стандартные частоты букв русского языка (33 буквы)
        # Частота Ё обычно низкая (~0.004), Е - (~0.055)
        self.russian_freq_with_Ё = [
            0.062,  # А
            0.014,  # Б
            0.041,  # В
            0.013,  # Г
            0.025,  # Д
            0.055,  # Е
            0.004,  # Ё (новая позиция)
            0.007,  # Ж
            0.016,  # З
            0.062,  # И
            0.010,  # Й
            0.028,  # К
            0.035,  # Л
            0.026,  # М
            0.053,  # Н
            0.090,  # О
            0.023,  # П
            0.040,  # Р
            0.045,  # С
            0.053,  # Т
            0.021,  # У
            0.002,  # Ф
            0.009,  # Х
            0.004,  # Ц
            0.012,  # Ч
            0.006,  # Ш
            0.003,  # Щ
            0.014,  # Ъ
            0.016,  # Ы
            0.014,  # Ь
            0.003,  # Э
            0.006,  # Ю
            0.018,  # Я
        ]

        self.russian_freq_with_no_Ё = [
            0.062,  # А
            0.014,  # Б
            0.041,  # В
            0.013,  # Г
            0.025,  # Д
            0.059,  # Е
            0.007,  # Ж
            0.016,  # З
            0.062,  # И
            0.010,  # Й
            0.028,  # К
            0.035,  # Л
            0.026,  # М
            0.053,  # Н
            0.090,  # О
            0.023,  # П
            0.040,  # Р
            0.045,  # С
            0.053,  # Т
            0.021,  # У
            0.002,  # Ф
            0.009,  # Х
            0.004,  # Ц
            0.012,  # Ч
            0.006,  # Ш
            0.003,  # Щ
            0.014,  # Ъ
            0.016,  # Ы
            0.014,  # Ь
            0.003,  # Э
            0.006,  # Ю
            0.018,  # Я
        ]

    def clean_text(self, text):
        """Очистка текста: удаление всех символов, кроме букв алфавита. Ё обрабатывается отдельно."""
        cleaned = []
        for char in text.upper():
            if char in self.alphabet:
                cleaned.append(char)

        return "".join(cleaned)

    def kasiski_test(self, text):
        """Тест Касиски для определения длины ключа"""
        trigrams = {}
        for i in range(len(text) - 2):
            trigram = text[i : i + 3]
            if trigram not in trigrams:
                trigrams[trigram] = []
            trigrams[trigram].append(i)

        distances = []
        for trigram, positions in trigrams.items():
            if len(positions) > 1:
                for i in range(len(positions)):
                    for j in range(i + 1, len(positions)):
                        distances.append(positions[j] - positions[i])

        if not distances:
            return 1

        def gcd(a, b):
            while b:
                a, b = b, a % b
            return a

        def gcd_list(numbers):
            if not numbers:
                return 1
            result = numbers[0]
            for num in numbers[1:]:
                result = gcd(result, num)
            return result

        candidate_period = gcd_list(distances)

        if candidate_period > 10:
            for i in range(10, 1, -1):
                if candidate_period % i == 0:
                    return i
            return 1

        return candidate_period if candidate_period > 0 else 1

    def index_of_coincidence(self, text):
        """Вычисление индекса совпадений"""
        if len(text) <= 1:
            return 0

        # Размер массива частот теперь self.alphabet_size = 33
        freq = [0] * self.alphabet_size
        for char in text:
            idx = self.alphabet.index(char)
            freq[idx] += 1

        total = 0
        for count in freq:
            total += count * (count - 1)

        n = len(text)
        return total / (n * (n - 1))

    def is_plausible_period(self, text, period):
        """Проверка, является ли период правдоподобным"""
        if period <= 0:
            return False

        total_ic = 0
        valid_cols = 0

        for offset in range(period):
            column = []
            for i in range(offset, len(text), period):
                column.append(text[i])

            if len(column) < 10:
                continue

            ic = self.index_of_coincidence("".join(column))
            total_ic += ic
            valid_cols += 1

        if valid_cols == 0:
            return False

        avg_ic = total_ic / valid_cols
        # Диапазон IC для русского языка (33 буквы): ~0.055
        return 0.05 < avg_ic < 0.075

    def estimate_period(self, text):
        """Оценка длины ключа"""
        kasiski_period = self.kasiski_test(text)

        if 2 <= kasiski_period <= 10 and self.is_plausible_period(text, kasiski_period):
            return kasiski_period

        best_ic = -1
        best_period = 1

        for period in range(1, 11):
            total_ic = 0
            valid_cols = 0

            for offset in range(period):
                column = []
                for i in range(offset, len(text), period):
                    column.append(text[i])

                if len(column) < 10:
                    continue

                ic = self.index_of_coincidence("".join(column))
                total_ic += ic
                valid_cols += 1

            if valid_cols == 0:
                continue

            avg_ic = total_ic / valid_cols

            # Учитываем только правдоподобные IC
            if 0.05 < avg_ic < 0.075:
                if avg_ic > best_ic:
                    best_ic = avg_ic
                    best_period = period

        return best_period

    def score_shifts(self, column):
        """Оценка сдвигов для одного столбца"""
        scores = []
        n = len(column)

        if n == 0:
            return scores

        col_freq = [0] * self.alphabet_size
        for char in column:
            idx = self.alphabet.index(char)
            col_freq[idx] += 1

        col_rel_freq = [count / n for count in col_freq]

        # Для каждого возможного сдвига (33 сдвига)
        for key_shift in range(self.alphabet_size):
            correlation = 0.0

            # Вычисляем корреляцию с эталонными частотами
            for char_idx in range(self.alphabet_size):
                # Вычисляем индекс буквы в открытом тексте
                plain_idx = (char_idx - key_shift) % self.alphabet_size

                # Используем относительную частоту столбца
                correlation += col_rel_freq[char_idx] * self.russian_freq[plain_idx]

            key_char = self.alphabet[key_shift]
            scores.append((key_char, correlation))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores

    def generate_key_candidates(self, text, period, top_n=3):
        """Генерация кандидатов в ключи"""
        columns = []
        for offset in range(period):
            column = []
            for i in range(offset, len(text), period):
                column.append(text[i])
            columns.append("".join(column))

        column_candidates = []
        for column in columns:
            candidates = self.score_shifts(column)
            column_candidates.append(candidates[:top_n])

        key_candidates = []

        def generate_combinations(current_key, current_score, depth):
            if depth == period:
                key_candidates.append((current_key, current_score))
                return

            if not column_candidates[depth]:
                return

            for char, score in column_candidates[depth]:
                generate_combinations(
                    current_key + char, current_score + score, depth + 1
                )

        generate_combinations("", 0, 0)
        key_candidates.sort(key=lambda x: x[1], reverse=True)

        return [key for key, score in key_candidates[:100]]

    def decrypt_with_punctuation(self, ciphertext, key):
        """Расшифровка с сохранением пунктуации и регистра"""

        # Очищаем ключ, чтобы он содержал только буквы из self.alphabet (теперь 33)
        cleaned_key = self.clean_text(key)

        if not cleaned_key:
            return ciphertext

        result = []
        key_index = 0

        for char in ciphertext:
            upper_char = char.upper()

            if upper_char in self.alphabet:
                # Индекс зашифрованного символа
                c_idx = self.alphabet.index(upper_char)

                # Индекс символа ключа (используем очищенный ключ)
                k_char = cleaned_key[key_index % len(cleaned_key)]
                k_idx = self.alphabet.index(k_char)

                # Вычисляем индекс символа открытого текста
                p_idx = (c_idx - k_idx) % self.alphabet_size
                plain_char = self.alphabet[p_idx]

                # Сохраняем оригинальный регистр
                if char.islower():
                    result.append(plain_char.lower())
                else:
                    result.append(plain_char)

                key_index += 1
            else:
                # Сохраняем пробелы, знаки препинания и другие символы
                result.append(char)

        return "".join(result)

    def validate_key(self, key):
        """Проверка ключа на корректность"""
        if not key:
            return False, "Ключ не может быть пустым"

        cleaned_key = self.clean_text(key)

        if not cleaned_key:
            return False, "Ключ должен содержать хотя бы одну русскую букву"

        return True, cleaned_key


class VigenereCrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Криптоанализ шифра Виженера")

        self.root.configure(bg="#f7f7f7")
        style = ttk.Style()
        style.theme_use("default")

        style.configure("TFrame", background="#f7f7f7")
        style.configure("TLabel", background="#f7f7f7", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10), padding=6)
        style.configure("TEntry", padding=4)
        style.configure(
            "Minimal.TLabelframe", background="#ffffff", borderwidth=1, relief="solid"
        )
        style.configure("Minimal.TLabelframe.Label", background="#ffffff")

        self.cracker = VigenereCracker()

        self.setup_ui()

    def setup_ui(self):
        main = ttk.Frame(self.root, padding=10)
        main.grid(row=0, column=0, sticky="nsew")

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        main.columnconfigure(0, weight=3)
        main.columnconfigure(1, weight=2)

        # ------------------ ЛЕВАЯ ЧАСТЬ ------------------
        left = ttk.Frame(main)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        left.columnconfigure(0, weight=1)

        ttk.Label(left, text="Шифротекст:", font=("Segoe UI", 11, "bold")).grid(
            row=0, column=0, sticky="w"
        )

        self.input_text = scrolledtext.ScrolledText(
            left, height=10, font=("Consolas", 10)
        )
        self.input_text.grid(row=1, column=0, sticky="nsew", pady=(4, 10))

        # кнопка анализировать + длина ключа
        control_frame = ttk.Frame(left)
        control_frame.grid(row=2, column=0, sticky="w", pady=5)

        ttk.Button(control_frame, text="Расшифровать", command=self.analyze).grid(
            row=0, column=0, padx=(0, 10)
        )

        ttk.Label(control_frame, text="Длина ключа:").grid(row=0, column=1)
        self.period_var = tk.StringVar(value="-")
        ttk.Label(
            control_frame, textvariable=self.period_var, font=("Segoe UI", 10, "bold")
        ).grid(row=0, column=2, padx=(5, 0))

        # ручной ввод ключа
        manual_key_frame = ttk.Frame(left)
        manual_key_frame.grid(row=3, column=0, sticky="w", pady=(10, 0))

        ttk.Label(manual_key_frame, text="Ручной ввод ключа:").grid(
            row=0, column=0, sticky="w"
        )

        self.manual_key_var = tk.StringVar()
        self.manual_key_entry = ttk.Entry(
            manual_key_frame, textvariable=self.manual_key_var, width=20
        )
        self.manual_key_entry.grid(row=0, column=1, padx=(10, 5))

        ttk.Button(
            manual_key_frame, text="Применить", command=self.apply_manual_key
        ).grid(row=0, column=2)

        # отображение текущего ключа
        self.current_key_var = tk.StringVar(value="Текущий ключ: не выбран")
        ttk.Label(left, textvariable=self.current_key_var, font=("Segoe UI", 9)).grid(
            row=4, column=0, sticky="w", pady=(5, 0)
        )

        # результат расшифровки
        ttk.Label(left, text="Результат:", font=("Segoe UI", 11, "bold")).grid(
            row=5, column=0, sticky="w", pady=(10, 0)
        )
        self.output_text = scrolledtext.ScrolledText(
            left, height=12, font=("Consolas", 10)
        )
        self.output_text.grid(row=6, column=0, sticky="nsew")

        left.rowconfigure(1, weight=1)
        left.rowconfigure(6, weight=2)

        # ------------------ ПРАВАЯ ЧАСТЬ ------------------
        right = ttk.LabelFrame(main, text="Ключи", style="Minimal.TLabelframe")
        right.grid(row=0, column=1, sticky="nsew")
        right.columnconfigure(0, weight=1)

        ttk.Label(right, text="Количество ключей:").grid(
            row=0, column=0, sticky="w", padx=10, pady=(5, 0)
        )
        self.keys_count_var = tk.StringVar(value="30")

        self.keys_count_entry = ttk.Entry(
            right, textvariable=self.keys_count_var, width=10
        )
        self.keys_count_entry.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="w")

        self.key_list = tk.Listbox(right, height=20, font=("Consolas", 10))
        self.key_list.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")

        self.key_list.bind("<<ListboxSelect>>", self.on_key_select)

        # кнопки для работы с ключами
        key_buttons_frame = ttk.Frame(right)
        key_buttons_frame.grid(row=3, column=0, padx=10, pady=(0, 5), sticky="ew")

        key_buttons_frame.columnconfigure(0, weight=1)
        key_buttons_frame.columnconfigure(1, weight=1)

        ttk.Button(
            key_buttons_frame, text="Копировать ключ", command=self.copy_selected_key
        ).grid(row=0, column=0, padx=2, sticky="ew")
        ttk.Button(
            key_buttons_frame, text="Вставить ключ", command=self.paste_to_manual
        ).grid(row=0, column=1, padx=2, sticky="ew")

        right.rowconfigure(2, weight=1)

    # ---------------- ЛОГИКА ----------------

    def analyze(self):
        ciphertext = self.input_text.get("1.0", "end").strip()
        if not ciphertext:
            messagebox.showwarning("Ошибка", "Введите шифротекст.")
            return

        if "е" in ciphertext or "Ё" in ciphertext:
            self.cracker.alphabet = self.cracker.alphabet_ё
            self.cracker.alphabet_size = 33
            self.cracker.russian_freq = self.cracker.russian_freq_with_Ё
        else:
            self.cracker.alphabet = self.cracker.alphabet_e
            self.cracker.alphabet_size = 32
            self.cracker.russian_freq = self.cracker.russian_freq_with_no_Ё

        cleaned = self.cracker.clean_text(ciphertext)
        if len(cleaned) < 20:
            messagebox.showwarning(
                "Ошибка", "Текст слишком короткий для анализа (нужно >20 букв)."
            )
            return

        # определяем длину ключа
        try:
            period = self.cracker.estimate_period(cleaned)
            self.period_var.set(str(period))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при оценке длины ключа: {e}")
            self.period_var.set("-")
            return

        # количество ключей
        try:
            n = int(self.keys_count_var.get())
            if n < 1 or n > 1000:
                raise ValueError
        except:
            messagebox.showerror("Ошибка", "Введите корректное число ключей (1-1000).")
            return

        # ищем ключи
        try:
            candidates = self.cracker.generate_key_candidates(cleaned, period, top_n=3)
            candidates = candidates[:n]
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при генерации ключей: {e}")
            candidates = []

        self.key_list.delete(0, "end")
        if not candidates:
            self.key_list.insert("end", "Ключи не найдены.")
            self.output_text.delete("1.0", "end")
            self.current_key_var.set("Текущий ключ: не выбран")
            return

        for i, k in enumerate(candidates, 1):
            self.key_list.insert("end", f"{i}. {k}")

        if candidates:
            self.key_list.selection_set(0)
            self.on_key_select(None)

    def on_key_select(self, event):
        """Обработка выбора ключа из списка"""
        if self.key_list.curselection():
            index = self.key_list.curselection()[0]
            item = self.key_list.get(index)
            if ". " in item:
                key = item.split(". ")[1]
            else:
                key = item

            self.current_key_var.set(f"Текущий ключ: {key}")
            self.decrypt_with_key(key)

    def apply_manual_key(self):
        """Применение ключа, введенного вручную"""
        key = self.manual_key_var.get().strip()

        if not key:
            messagebox.showwarning("Ошибка", "Введите ключ.")
            return

        is_valid, cleaned_key = self.cracker.validate_key(key)

        if not is_valid:
            messagebox.showerror("Ошибка", cleaned_key)
            return

        self.current_key_var.set(f"Текущий ключ: {cleaned_key}")
        self.decrypt_with_key(cleaned_key)

        self.manual_key_var.set(cleaned_key)

        key_str = cleaned_key
        items = self.key_list.get(0, "end")
        if not any(key_str in item for item in items):
            self.key_list.insert(0, f"Ручной. {key_str}")
            self.key_list.selection_clear(0, "end")
            self.key_list.selection_set(0)

    def decrypt_with_key(self, key):
        """Расшифровка с использованием указанного ключа"""
        text = self.input_text.get("1.0", "end").strip()
        if not text:
            return

        try:
            # decrypt_with_punctuation сам очистит ключ для использования
            result = self.cracker.decrypt_with_punctuation(text, key)
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", result)
        except Exception as e:
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", f"Ошибка расшифровки: {e}")

    def copy_selected_key(self):
        """Копирование выбранного ключа в буфер обмена"""
        if self.key_list.curselection():
            index = self.key_list.curselection()[0]
            item = self.key_list.get(index)
            if ". " in item:
                key = item.split(". ")[1]
            else:
                key = item
            self.root.clipboard_clear()
            self.root.clipboard_append(key)
            messagebox.showinfo("Успех", f"Ключ '{key}' скопирован в буфер обмена")

    def paste_to_manual(self):
        """Вставка ключа из буфера обмена в поле ручного ввода"""
        try:
            clipboard_content = self.root.clipboard_get()
            if clipboard_content:
                cleaned_content = self.cracker.clean_text(clipboard_content)
                self.manual_key_var.set(cleaned_content)
        except:
            messagebox.showwarning(
                "Ошибка", "Не удалось получить данные из буфера обмена"
            )


def main():
    root = tk.Tk()
    root.geometry("1000x700")
    VigenereCrackerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
