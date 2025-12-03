import math
from collections import Counter
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog

# --- КОНСТАНТЫ РУССКОГО АЛФАВИТА ---
RUSSIAN_ALPHABET = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
ALPHABET_SIZE = len(RUSSIAN_ALPHABET)

RUSSIAN_FREQUENCIES = [
    0.0801,
    0.0159,
    0.0454,
    0.017,
    0.0298,
    0.0845,
    0.0094,
    0.0165,
    0.0735,
    0.0121,
    0.0349,
    0.044,
    0.0321,
    0.067,
    0.1097,
    0.028,
    0.0474,
    0.0547,
    0.0626,
    0.0262,
    0.0026,
    0.009,
    0.0048,
    0.0144,
    0.0073,
    0.0036,
    0.0004,
    0.019,
    0.0174,
    0.0032,
    0.0064,
    0.0193,
]
# Рассчитывает ожидаемый Индекс Совпадения для русского языка
EXPECTED_IC_RU = sum(p**2 for p in RUSSIAN_FREQUENCIES)  # ≈ 0.0553


# --- КЛАСС КРИПТОАНАЛИЗАТОРА (Логика) ---
class VigenereCrackerLogic:
    def __init__(self, alphabet, frequencies, expected_ic):
        self.alphabet = alphabet
        self.size = len(alphabet)
        self.frequencies = frequencies
        self.expected_ic = expected_ic
        self.char_to_index = {char: i for i, char in enumerate(alphabet)}
        self.index_to_char = {i: char for i, char in enumerate(alphabet)}

        # Атрибут для хранения структуры оригинального текста (для восстановления пунктуации)
        self.original_structure = []

        # Результаты последнего анализа
        self.last_key_results = []
        self.cleaned_ciphertext = ""

    # --- ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ (Обновлены для сохранения пунктуации) ---

    def _clean_ciphertext(self, ciphertext):
        """
        Очищает текст, сохраняя карту оригинальной структуры (punctuations, spaces, etc.).
        Возвращает: очищенный текст (str).
        Заполняет: self.original_structure (list).
        """
        cleaned_text = []
        self.original_structure = []

        for char in ciphertext:
            upper_char = char.upper()
            if upper_char in self.alphabet:
                cleaned_text.append(upper_char)
                self.original_structure.append(None)  # Флаг для буквы
            else:
                self.original_structure.append(char)

        return "".join(cleaned_text)

    def _calculate_ic(self, text):
        n = len(text)
        if n < 2:
            return 0.0
        counts = Counter(text)
        ic_sum = sum(count * (count - 1) for count in counts.values())
        return ic_sum / (n * (n - 1))

    def _calculate_chi_squared(self, frequency_vector, total_chars):
        if total_chars == 0:
            return float("inf")
        chi_squared_sum = 0
        for i in range(self.size):
            expected_count = self.frequencies[i] * total_chars
            if expected_count > 0:
                chi_squared_sum += (
                    frequency_vector[i] - expected_count
                ) ** 2 / expected_count
        return chi_squared_sum

    def _decrypt(self, ciphertext, key):
        """Расшифровывает чистый текст с заданным ключом."""
        decrypted_text = ""
        key_length = len(key)
        for i, cipher_char in enumerate(ciphertext):
            key_char = key[i % key_length]
            cipher_index = self.char_to_index[cipher_char]
            key_index = self.char_to_index[key_char]

            # P = (C - K) mod N
            plain_index = (cipher_index - key_index) % self.size
            decrypted_text += self.index_to_char[plain_index]

        return decrypted_text

    def _restore_punctuation(self, decrypted_clean_text):
        """
        Восстанавливает пунктуацию и пробелы, используя сохраненную карту.
        """
        restored_text = []
        decrypted_index = 0

        for item in self.original_structure:
            if item is None:
                if decrypted_index < len(decrypted_clean_text):
                    # Вставляем расшифрованную букву
                    restored_text.append(decrypted_clean_text[decrypted_index])
                    decrypted_index += 1
                else:
                    break
            else:
                # Вставляем пунктуацию или пробел
                restored_text.append(item)

        return "".join(restored_text)

    # --- ТЕСТ КАСИСКИ И IC ---
    def _kassiski_test(self, ciphertext, max_key_len=10, min_seq_len=3):
        # Реализация теста Касиски
        n = len(ciphertext)
        repetitions = {}
        for length in range(min_seq_len, 8):
            for i in range(n - length + 1):
                sequence = ciphertext[i : i + length]
                if sequence not in repetitions:
                    repetitions[sequence] = []
                repetitions[sequence].append(i)

        repeating_sequences = {
            seq: positions
            for seq, positions in repetitions.items()
            if len(positions) > 1
        }
        differences = []
        for seq, positions in repeating_sequences.items():
            for i in range(len(positions) - 1):
                differences.append(positions[i + 1] - positions[i])
        if not differences:
            return []

        divisor_counts = Counter()
        for diff in differences:
            for i in range(1, int(math.sqrt(diff)) + 1):
                if diff % i == 0:
                    for d in [i, diff // i]:
                        # проверка на длину делителя(подходящего ключа)
                        if d > 1 and d <= max_key_len:
                            divisor_counts[d] += 1
        return divisor_counts.most_common(5)

    def _verify_key_length_ic(self, ciphertext, key_length):
        columns = [ciphertext[i::key_length] for i in range(key_length)]
        avg_ic = sum(self._calculate_ic(col) for col in columns) / key_length
        ic_difference = abs(avg_ic - self.expected_ic)
        return avg_ic, ic_difference < 0.02

    def _find_key_length(self, ciphertext):
        output = []
        best_m = 0

        output.append("--- 1. Тест Касиски и IC: Определение длины ключа (m) ---")

        key_candidates = self._kassiski_test(ciphertext)

        if not key_candidates:
            output.append("Тест Касиски не дал результатов. Переход к полному подбору.")
            candidate_lengths = [(m, 0) for m in range(2, 16)]
        else:
            output.append(
                "Кандидаты Касиски (топ-5): "
                + ", ".join(f"m={m}" for m, c in key_candidates)
            )
            candidate_lengths = key_candidates

        for m, _ in candidate_lengths:
            avg_ic, is_confirmed = self._verify_key_length_ic(ciphertext, m)
            status = "ПОДТВЕРЖДЕН" if is_confirmed else "НЕ ПОДТВЕРЖДЕН"
            output.append(f"  m={m}: IC={avg_ic:.5f} ({status})")
            if is_confirmed:
                best_m = m
                break

        if best_m == 0:
            output.append(
                "\nIC не подтвержден. Выполняется подбор лучшего IC (m=2..15)..."
            )
            best_ic_diff = float("inf")

            for m in range(2, 16):
                avg_ic = sum(self._calculate_ic(ciphertext[i::m]) for i in range(m)) / m
                ic_diff = abs(avg_ic - self.expected_ic)
                if ic_diff < best_ic_diff:
                    best_ic_diff = ic_diff
                    best_m = m

            if best_m > 0:
                output.append(
                    f"Подбором выбрана длина: **m = {best_m}** (Avg IC: {self._verify_key_length_ic(ciphertext, best_m)[0]:.5f})"
                )
            else:
                output.append(
                    "Не удалось найти подходящую длину ключа в диапазоне 2-15."
                )

        self.output_text = "\n".join(output)
        return best_m

    # --- МЕТОДЫ MIC И АНАЛИЗ КЛЮЧА ---
    def _calculate_mic(self, text1, text2, shift_2):
        n1 = len(text1)
        n2 = len(text2)
        if n1 == 0 or n2 == 0:
            return 0.0
        counts1 = Counter(text1)
        counts2 = Counter(text2)
        mic_sum = 0
        for i in range(self.size):
            char1 = self.index_to_char[i]
            shifted_index = (i - shift_2) % self.size
            char2_shifted = self.index_to_char[shifted_index]
            mic_sum += counts1[char1] * counts2[char2_shifted]
        return mic_sum / (n1 * n2)

    def analyze_key(self, ciphertext, key_length):
        output = []
        columns = [ciphertext[i::key_length] for i in range(key_length)]
        column_1 = columns[0]
        relative_shifts = {1: 0}

        output.append(
            f"\n--- 2. MIC: Определение относительных сдвигов для m={key_length} ---"
        )

        for i in range(1, key_length):
            column_i = columns[i]
            best_mic = 0.0
            best_shift = 0
            for shift in range(self.size):
                mic = self._calculate_mic(column_1, column_i, shift)
                if mic > best_mic:
                    best_mic = mic
                    best_shift = shift

            output.append(
                f"  - Столбец {i+1}: Относительный сдвиг **{best_shift}** (MIC={best_mic:.5f})"
            )
            relative_shifts[i + 1] = best_shift

        all_key_results = []
        for g1_shift in range(self.size):
            key = ""
            for i in range(1, key_length + 1):
                g_i_shift = (g1_shift - relative_shifts[i]) % self.size
                key += self.index_to_char[g_i_shift]
            print(key)

            decrypted_clean_text = self._decrypt(
                ciphertext, key
            )  # Получаем чистый текст

            full_text_counts = Counter(decrypted_clean_text)
            ordered_frequency_vector = [
                full_text_counts[char] for char in self.alphabet
            ]
            chi_squared_val = self._calculate_chi_squared(
                ordered_frequency_vector, len(decrypted_clean_text)
            )

            all_key_results.append(
                {
                    "key": key,
                    "chi2": chi_squared_val,
                    # !!! КЛЮЧЕВОЙ МОМЕНТ: Сохраняем чистый текст под нужным ключом
                    "decrypted_clean_text": decrypted_clean_text,
                    "g1_shift": g1_shift,
                }
            )

        print(all_key_results)

        all_key_results.sort(key=lambda x: x["chi2"])
        self.last_key_results = all_key_results
        self.output_text += "\n" + "\n".join(output)

        return all_key_results[:5]


# --- КЛАСС ГРАФИЧЕСКОГО ИНТЕРФЕЙСА (GUI) ---


class VigenereCrackerGUI:
    def __init__(self, master):
        self.master = master
        master.title("Vigenere Cracker (Русский)")
        self.cracker_logic = VigenereCrackerLogic(
            RUSSIAN_ALPHABET, RUSSIAN_FREQUENCIES, EXPECTED_IC_RU
        )

        self.key_options = tk.StringVar(master)
        self.key_options.set("Выберите ключ для расшифровки")
        self.current_key_results = []

        self.create_widgets()

    def create_widgets(self):
        # 1. Ввод шифротекста и кнопка загрузки
        input_frame = tk.Frame(self.master)
        input_frame.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        tk.Label(input_frame, text="1. Шифротекст (Ciphertext):").pack(side=tk.LEFT)

        # КНОПКА ЗАГРУЗКИ ФАЙЛА
        self.load_button = tk.Button(
            input_frame,
            text="Загрузить из файла",
            command=self.load_file_from_dialog,
        )
        self.load_button.pack(side=tk.LEFT, padx=(20, 0))

        # Поле ввода шифротекста (исправлено на state=tk.NORMAL)
        self.cipher_input = scrolledtext.ScrolledText(
            self.master, height=10, width=60, wrap=tk.WORD, state=tk.NORMAL
        )
        self.cipher_input.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        # 2. Кнопка Анализа
        self.analyze_button = tk.Button(
            self.master,
            text="2. АНАЛИЗИРОВАТЬ",
            command=self.run_analysis,
            bg="lightblue",
            font=("Arial", 10, "bold"),
        )
        self.analyze_button.grid(row=2, column=0, columnspan=2, pady=10)

        # 3. Вывод Анализа (Логи)
        tk.Label(self.master, text="3. Анализ (Длина ключа, IC, MIC, Chi^2):").grid(
            row=3, column=0, sticky="w", padx=5, pady=5
        )
        self.analysis_output = scrolledtext.ScrolledText(
            self.master, height=10, width=60, wrap=tk.WORD, state=tk.DISABLED
        )
        self.analysis_output.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # 4. Выбор Ключа (DropDown)
        tk.Label(self.master, text="4. Выбрать ключ (по Chi^2):").grid(
            row=5, column=0, sticky="w", padx=5, pady=5
        )
        self.key_dropdown = tk.OptionMenu(
            self.master, self.key_options, "Выберите ключ для расшифровки"
        )
        self.key_dropdown.config(width=50)
        self.key_dropdown.grid(row=6, column=0, sticky="w", padx=5, pady=5)

        self.decrypt_button = tk.Button(
            self.master,
            text="РАСШИФРОВАТЬ",
            command=self.run_decryption,
            bg="lightgreen",
        )
        self.decrypt_button.grid(row=6, column=1, sticky="w", padx=5, pady=5)

        # 5. Вывод Расшифрованного Текста
        tk.Label(self.master, text="5. Расшифрованный текст (Decrypted Text):").grid(
            row=7, column=0, sticky="w", padx=5, pady=5
        )
        self.decrypted_output = scrolledtext.ScrolledText(
            self.master, height=10, width=60, wrap=tk.WORD, state=tk.DISABLED
        )
        self.decrypted_output.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

    def load_file_from_dialog(self):
        """Открывает диалог выбора файла, читает содержимое и вставляет его в поле шифротекста."""

        file_path = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")],
        )

        if not file_path:
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            self.cipher_input.delete("1.0", tk.END)
            self.cipher_input.insert("1.0", content)

            messagebox.showinfo(
                "Готово", f"Файл '{file_path.split('/')[-1]}' успешно загружен."
            )

        except Exception as e:
            messagebox.showerror("Ошибка загрузки", f"Не удалось прочитать файл:\n{e}")

    def update_output(self, text):
        """Обновляет поле вывода анализа."""
        self.analysis_output.config(state=tk.NORMAL)
        self.analysis_output.delete("1.0", tk.END)
        self.analysis_output.insert(tk.END, text)
        self.analysis_output.config(state=tk.DISABLED)

    def update_decrypted_output(self, text):
        """Обновляет поле расшифрованного текста."""
        self.decrypted_output.config(state=tk.NORMAL)
        self.decrypted_output.delete("1.0", tk.END)
        self.decrypted_output.insert(tk.END, text)
        self.decrypted_output.config(state=tk.DISABLED)

    def run_analysis(self):
        """Обрабатывает нажатие кнопки "АНАЛИЗИРОВАТЬ"."""
        raw_ciphertext = self.cipher_input.get("1.0", tk.END).strip()

        if not raw_ciphertext:
            messagebox.showerror("Ошибка", "Введите шифротекст для анализа.")
            return

        # Очистка и сохранение структуры пунктуации
        cleaned_ciphertext = self.cracker_logic._clean_ciphertext(raw_ciphertext)
        self.cracker_logic.cleaned_ciphertext = cleaned_ciphertext

        if len(cleaned_ciphertext) < 50:
            messagebox.showwarning(
                "Внимание",
                "Текст слишком короткий (<50 символов) для надежного анализа.",
            )

        m = self.cracker_logic._find_key_length(cleaned_ciphertext)

        if m == 0:
            self.update_output(
                self.cracker_logic.output_text
                + "\n\nНе удалось определить длину ключа m."
            )
            return

        top_results = self.cracker_logic.analyze_key(cleaned_ciphertext, m)

        analysis_text = (
            self.cracker_logic.output_text
            + f"\n\nОкончательно выбрана длина ключа **m = {m}**"
        )
        analysis_text += "\n\n--- 3. Топ-5 кандидатов ключа (по Chi-Squared) ---"

        key_options_list = []
        for i, res in enumerate(top_results):
            option_str = f"Ключ: {res['key']} | Chi^2: {res['chi2']:.2f}"
            analysis_text += f"\nВАРИАНТ #{i+1}: {option_str} | g[1]={self.cracker_logic.index_to_char[res['g1_shift']]}"
            key_options_list.append((option_str, res["key"]))

        self.update_output(analysis_text)

        self.current_key_results = key_options_list
        menu = self.key_dropdown["menu"]
        menu.delete(0, "end")
        self.key_options.set("Выберите ключ для расшифровки")
        for option_str, key in key_options_list:
            menu.add_command(
                label=option_str, command=tk._setit(self.key_options, option_str)
            )

    def run_decryption(self):
        """Обрабатывает нажатие кнопки "РАСШИФРОВАТЬ"."""
        selected_option = self.key_options.get()

        if (
            "Выберите ключ" in selected_option
            or not self.cracker_logic.cleaned_ciphertext
            or not self.cracker_logic.last_key_results
        ):
            messagebox.showerror(
                "Ошибка", "Сначала проведите анализ и выберите ключ из списка."
            )
            return

        key_to_use = None
        decrypted_clean_text = None

        # Извлекаем ключ из выбранной строки (например, "Ключ: СЛОВО | Chi^2: 123.45")
        selected_key_str = selected_option.split(" | Chi^2:")[0].replace("Ключ: ", "")

        # Ищем в полных результатах ключ и соответствующий ему чистый текст
        for res in self.cracker_logic.last_key_results:
            if res["key"] == selected_key_str:
                key_to_use = res["key"]
                # !!! ИСПРАВЛЕНИЕ: Используем 'decrypted_clean_text'
                decrypted_clean_text = res["decrypted_clean_text"]
                break

        if key_to_use is None:
            messagebox.showerror(
                "Ошибка", "Не удалось найти ключ в результатах. Повторите анализ."
            )
            return

        # Восстановление пунктуации и пробелов
        decrypted_text_with_punc = self.cracker_logic._restore_punctuation(
            decrypted_clean_text
        )

        # Вывод
        self.update_decrypted_output(
            f"ИСПОЛЬЗУЕМЫЙ КЛЮЧ: {key_to_use}\n\n" + decrypted_text_with_punc
        )


# --- ГЛАВНАЯ ФУНКЦИЯ ЗАПУСКА ---

if __name__ == "__main__":
    root = tk.Tk()
    app = VigenereCrackerGUI(root)
    root.mainloop()
