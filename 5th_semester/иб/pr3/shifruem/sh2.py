import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog, font
import math
import collections
import itertools


ALPHABET = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
ALPHABET_SIZE = len(ALPHABET)

RUSSIAN_FREQUENCIES = {
    "О": 0.1098,
    "Е": 0.0848,
    "А": 0.0799,
    "И": 0.0736,
    "Н": 0.0670,
    "Т": 0.0631,
    "С": 0.0547,
    "Р": 0.0474,
    "В": 0.0453,
    "Л": 0.0434,
    "К": 0.0348,
    "М": 0.0320,
    "Д": 0.0297,
    "П": 0.0280,
    "У": 0.0261,
    "Я": 0.0200,
    "Ы": 0.0189,
    "Ь": 0.0173,
    "Г": 0.0168,
    "З": 0.0164,
    "Б": 0.0159,
    "Ч": 0.0145,
    "Й": 0.0120,
    "Х": 0.0096,
    "Ж": 0.0094,
    "Ш": 0.0071,
    "Ю": 0.0063,
    "Ц": 0.0048,
    "Щ": 0.0036,
    "Э": 0.0033,
    "Ф": 0.0026,
    "Ъ": 0.0003,
}


def filter_text(ciphertext):
    return "".join([char.upper() for char in ciphertext if char.upper() in ALPHABET])


def kasiski_examination(ciphertext, min_len=3, max_len=5):
    distances = []
    for seq_len in range(max_len, min_len - 1, -1):
        sequences = {}
        for i in range(len(ciphertext) - seq_len + 1):
            seq = ciphertext[i : i + seq_len]
            if seq in sequences:
                sequences[seq].append(i)
            else:
                sequences[seq] = [i]
        for seq in sequences:
            if len(sequences[seq]) > 1:
                pos = sequences[seq]
                for i in range(len(pos) - 1):
                    distances.append(pos[i + 1] - pos[i])
    if not distances:
        return []
    factors = collections.Counter()
    for dist in distances:
        for i in range(2, int(math.sqrt(dist)) + 1):
            if dist % i == 0:
                factors[i] += 1
                if i * i != dist:
                    factors[dist // i] += 1
        if dist > 1:
            factors[dist] += 1
    return [item[0] for item in factors.most_common(5)]


def calculate_ioc(text):
    n = len(text)
    if n < 2:
        return 0.0
    counts = collections.Counter(text)
    ioc_sum = sum(count * (count - 1) for count in counts.values())
    return ioc_sum / (n * (n - 1))


def find_key_length_ioc(ciphertext, max_len=10):
    ioc_by_length = {}
    for length in range(2, max_len + 1):
        columns = [""] * length
        for i, char in enumerate(ciphertext):
            columns[i % length] += char
        total_ioc = sum(calculate_ioc(col) for col in columns)
        ioc_by_length[length] = total_ioc / length
    return ioc_by_length


"""
def generate_key_candidates(ciphertext, key_length, num_candidates=3):
    column_candidates = []
    columns = [""] * key_length
    for i, char in enumerate(ciphertext):
        columns[i % key_length] += char

    for col in columns:
        shift_scores = []
        if not col:
            continue
        for shift in range(ALPHABET_SIZE):
            decrypted_col = "".join(
                [
                    ALPHABET[
                        (ALPHABET.find(char) - shift + ALPHABET_SIZE) % ALPHABET_SIZE
                    ]
                    for char in col
                ]
            )
            counts = collections.Counter(decrypted_col)
            chi_squared = 0
            for letter in ALPHABET:
                observed = counts.get(letter, 0)
                expected = len(col) * RUSSIAN_FREQUENCIES.get(letter, 0)
                if expected > 0:
                    chi_squared += (observed - expected) ** 2 / expected
            shift_scores.append((chi_squared, ALPHABET[shift]))

        shift_scores.sort()

        top_letters = [letter for score, letter in shift_scores[:num_candidates]]
        column_candidates.append(top_letters)

    if len(column_candidates) != key_length:
        return []

    key_combinations = list(itertools.product(*column_candidates))
    candidate_keys = ["".join(combo) for combo in key_combinations]
    return candidate_keys
"""


def generate_key_candidates(ciphertext, key_length, num_candidates=3):
    # ... (код для создания columns остается без изменений) ...
    column_candidates = []
    columns = [""] * key_length
    for i, char in enumerate(ciphertext):
        columns[i % key_length] += char

    for col in columns:
        shift_scores = []
        if not col:
            continue
        col_len = len(col)

        for shift in range(ALPHABET_SIZE):
            decrypted_col = "".join(
                [
                    ALPHABET[
                        (ALPHABET.find(char) - shift + ALPHABET_SIZE) % ALPHABET_SIZE
                    ]
                    for char in col
                ]
            )

            counts = collections.Counter(decrypted_col)
            # --- РАСЧЕТ ИНДЕКСА ВЗАИМНОГО СООТВЕТСТВИЯ (MIC) ---
            mic_score = 0
            for letter_index in range(ALPHABET_SIZE):
                letter = ALPHABET[letter_index]
                observed_freq = counts.get(letter, 0) / col_len
                expected_prob = RUSSIAN_FREQUENCIES.get(letter, 0)

                # MIC = Сумма (Наблюдаемая_Частота * Ожидаемая_Вероятность)
                mic_score += observed_freq * expected_prob

            # В отличие от Chi-squared, мы ищем МАКСИМУМ MIC
            shift_scores.append((mic_score, ALPHABET[shift]))

        # Сортируем по убыванию (максимальный MIC в начале)
        shift_scores.sort(key=lambda x: x[0], reverse=True)

        top_letters = [letter for score, letter in shift_scores[:num_candidates]]
        column_candidates.append(top_letters)

    if len(column_candidates) != key_length:
        return []

    key_combinations = list(itertools.product(*column_candidates))
    candidate_keys = ["".join(combo) for combo in key_combinations]
    return candidate_keys


def vigenere_decrypt_with_formatting(raw_ciphertext, key):
    decrypted_text = []
    key_length = len(key)
    key_char_index = 0
    for char in raw_ciphertext:
        char_upper = char.upper()
        if char_upper in ALPHABET:
            char_pos = ALPHABET.find(char_upper)
            key_pos = ALPHABET.find(key[key_char_index % key_length])
            decrypted_pos = (char_pos - key_pos + ALPHABET_SIZE) % ALPHABET_SIZE
            decrypted_char = ALPHABET[decrypted_pos]
            if char.islower():
                decrypted_text.append(decrypted_char.lower())
            else:
                decrypted_text.append(decrypted_char)
            key_char_index += 1
        else:
            decrypted_text.append(char)
    return "".join(decrypted_text)


class VigenereCrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Как сломать шифр Вижинера???")
        self.root.geometry("900x750")
        self.root.minsize(800, 600)
        # self.setup_styles()
        self.create_menu()
        main_frame = ttk.Frame(root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.grid_rowconfigure(2, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        self.create_input_widgets(main_frame)
        self.create_control_widgets(main_frame)
        self.create_results_widgets(main_frame)

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Загрузить шифротекст...", command=self.load_file)
        file_menu.add_command(label="Сохранить результат...", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)

    def create_input_widgets(self, parent):
        left_frame = ttk.Frame(parent)
        left_frame.grid(row=0, column=0, rowspan=3, sticky="nswe")
        left_frame.grid_rowconfigure(1, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)

        input_frame = ttk.LabelFrame(left_frame, text="Шифротекст")
        input_frame.grid(row=0, column=0, sticky="nwe")
        input_frame.grid_columnconfigure(0, weight=1)

        self.ciphertext_input = scrolledtext.ScrolledText(
            input_frame, height=15, wrap=tk.WORD
        )

        self.ciphertext_input.grid(row=0, column=0, sticky="nsew")

        load_button = ttk.Button(
            input_frame, text="Открыть файл", command=self.load_file
        )

        load_button.grid(row=1, column=0, sticky="w")

    def create_control_widgets(self, parent):
        left_control = ttk.LabelFrame(parent, text="Анализ")
        left_control.grid(row=1, column=0, sticky="we", pady=5)
        left_control.grid_columnconfigure(0, weight=1)

        ttk.Button(
            left_control, text="Длина ключа", command=self.analyze_key_length
        ).pack(fill="x", pady=4)

        ttk.Button(
            left_control, text="Варианты ключа", command=self.show_key_candidates
        ).pack(fill="x", pady=4)

        ttk.Button(
            left_control, text="Расшифровать", command=self.decrypt_message
        ).pack(fill="x", pady=4)

    def create_results_widgets(self, parent):
        right = ttk.LabelFrame(parent, text="Вывод")
        right.grid(row=0, column=1, rowspan=3, sticky="nsew")
        right.grid_rowconfigure(5, weight=1)
        right.grid_columnconfigure(0, weight=1)

        ttk.Label(right, text="Возможные периоды:").grid(row=0, column=0, sticky="w")

        ttk.Label(right, text="Индекс совпадений:").grid(
            row=2, column=0, sticky="w", padx=5
        )

        cols = ("length", "ioc")
        self.ioc_tree = ttk.Treeview(right, columns=cols, show="headings")
        self.ioc_tree.heading("length", text="Дл.")
        self.ioc_tree.heading("ioc", text="IoC")
        self.ioc_tree.column("length", width=50, anchor="center")
        self.ioc_tree.column("ioc", width=100, anchor="center")
        self.ioc_tree.grid(row=3, column=0, sticky="nwe")

        ttk.Label(right, text="Длина ключа:").grid(row=4, column=0, sticky="w")
        self.key_length_var = tk.StringVar()
        self.key_length_entry = ttk.Entry(
            right, textvariable=self.key_length_var, width=8
        )
        self.key_length_entry.grid(row=5, column=0, sticky="w", padx=10, pady=(0, 10))

        ttk.Label(right, text="Ключ:").grid(row=6, column=0, sticky="w")
        self.key_var = tk.StringVar()
        self.key_entry = ttk.Entry(right, textvariable=self.key_var)
        self.key_entry.grid(row=7, column=0, sticky="we", padx=5, pady=5)

        ttk.Label(right, text="Варианты:").grid(row=8, column=0, sticky="w")
        self.key_candidates_output = scrolledtext.ScrolledText(
            right, height=5, wrap=tk.WORD
        )
        self.key_candidates_output.grid(row=9, column=0, sticky="nsew", padx=5, pady=5)

        ttk.Label(right, text="Расшифровка:").grid(row=10, column=0, sticky="w", padx=5)
        self.plaintext_output = scrolledtext.ScrolledText(right, wrap=tk.WORD)
        self.plaintext_output.grid(row=11, column=0, sticky="nsew", padx=5, pady=5)

    def load_file(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if not filepath:
            return
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                self.ciphertext_input.delete("1.0", tk.END)
                self.ciphertext_input.insert("1.0", content)
        except Exception as e:
            messagebox.showerror(
                "Ошибка чтения файла", f"Не удалось прочитать файл:\n{e}"
            )

    def save_file(self):
        content = self.plaintext_output.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning(
                "Нечего сохранять", "Поле с расшифрованным текстом пусто."
            )
            return
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        )
        if not filepath:
            return
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            messagebox.showinfo("Успех", "Файл успешно сохранен.")
        except Exception as e:
            messagebox.showerror(
                "Ошибка сохранения", f"Не удалось сохранить файл:\n{e}"
            )

    def analyze_key_length(self):
        ciphertext = filter_text(self.ciphertext_input.get("1.0", tk.END))
        if not ciphertext:
            messagebox.showerror("Ошибка", "Введите или загрузите шифротекст.")
            return

        ioc_results = find_key_length_ioc(ciphertext)
        self.ioc_tree.delete(*self.ioc_tree.get_children())
        best_len, max_ioc, best_item_id = 0, 0, None
        for length, ioc in sorted(ioc_results.items()):
            item_id = self.ioc_tree.insert("", tk.END, values=(length, f"{ioc:.5f}"))
            if ioc > max_ioc:
                max_ioc, best_len, best_item_id = ioc, length, item_id
        if best_item_id:
            self.ioc_tree.selection_set(best_item_id)
            self.ioc_tree.focus(best_item_id)
            self.ioc_tree.see(best_item_id)
        self.key_length_var.set(str(best_len))

    def show_key_candidates(self):
        ciphertext = filter_text(self.ciphertext_input.get("1.0", tk.END))
        try:
            key_length = int(self.key_length_var.get())
        except ValueError:
            messagebox.showerror(
                "Ошибка", "Укажите корректную длину ключа (целое число)."
            )
            return
        if not ciphertext or key_length <= 0:
            return

        candidate_keys = generate_key_candidates(ciphertext, key_length)
        self.key_candidates_output.delete("1.0", tk.END)
        if candidate_keys:
            self.key_candidates_output.insert("1.0", "\n".join(candidate_keys))
            self.key_var.set(candidate_keys[0])
        else:
            self.key_candidates_output.insert(
                "1.0", "Не удалось сгенерировать варианты."
            )

    def decrypt_message(self):
        raw_ciphertext = self.ciphertext_input.get("1.0", tk.END)
        key = self.key_var.get().upper()
        if not raw_ciphertext.strip() or not key:
            messagebox.showerror(
                "Ошибка", "Введите шифротекст и выберите/введите ключ."
            )
            return
        plaintext = vigenere_decrypt_with_formatting(raw_ciphertext, key)
        self.plaintext_output.delete("1.0", tk.END)
        self.plaintext_output.insert("1.0", plaintext)


if __name__ == "__main__":
    root = tk.Tk()
    app = VigenereCrackerApp(root)
    root.mainloop()
