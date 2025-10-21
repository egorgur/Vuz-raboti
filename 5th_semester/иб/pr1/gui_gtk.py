import traceback
from cipher import MagicSquareCipher
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib
import numpy as np
import threading
import random


class CipherGUI:
    """Графический интерфейс для шифровальщика на GTK"""

    def __init__(self, cipher: MagicSquareCipher):
        self.cipher = cipher
        self.setup_theme()
        self.create_ui()

    def setup_theme(self):
        """Настройка темы в соответствии с системой"""
        settings = Gtk.Settings.get_default()
        self.detect_system_theme()
        settings.set_property("gtk-application-prefer-dark-theme", self.prefers_dark)

    def detect_system_theme(self):
        """Определение системной темы"""
        settings = Gtk.Settings.get_default()
        current_theme = settings.get_property("gtk-theme-name")
        print(f"Текущая тема GTK: {current_theme}")
        self.prefers_dark = settings.get_property("gtk-application-prefer-dark-theme")

        display = Gdk.Display.get_default()
        if display:
            app = Gtk.Application.get_default()
            if app:
                app.prefers_color_scheme = (
                    Gtk.SettingsColorScheme.PREFER_DARK
                    if self.prefers_dark
                    else Gtk.SettingsColorScheme.PREFER_LIGHT
                )

    def create_ui(self):
        """Создание пользовательского интерфейса"""
        # Главное окно
        self.window = Gtk.Window(
            title="Шифр на основе магических квадратов"
        )
        self.window.set_default_size(1000, 800)
        self.window.connect("destroy", Gtk.main_quit)

        # Основной контейнер
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_box.set_margin_top(10)
        main_box.set_margin_bottom(10)
        main_box.set_margin_start(10)
        main_box.set_margin_end(10)
        self.window.add(main_box)

        # Ноутбук (вкладки)
        self.notebook = Gtk.Notebook()
        main_box.pack_start(self.notebook, True, True, 0)

        # Создание вкладок
        self.create_encrypt_tab()
        self.create_square_tab()

        # Статусная строка
        self.status_bar = Gtk.Statusbar()
        self.status_context_id = self.status_bar.get_context_id("main")
        main_box.pack_start(self.status_bar, False, False, 0)

        self.window.show_all()

    def create_square_tab(self):
        """Создание вкладки для управления магическим квадратом"""
        square_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        square_box.set_margin_top(10)
        square_box.set_margin_bottom(10)
        square_box.set_margin_start(10)
        square_box.set_margin_end(10)

        # Фрейм выбора типа квадрата
        type_frame = Gtk.Frame(label="Тип магического квадрата")
        type_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        type_frame.add(type_box)

        self.square_type_combo = Gtk.ComboBoxText()
        self.square_type_combo.append_text("Сгенерировать автоматически")
        self.square_type_combo.append_text("Ввести вручную")
        self.square_type_combo.set_active(0)
        self.square_type_combo.connect("changed", self.on_square_type_changed)
        type_box.pack_start(self.square_type_combo, False, False, 0)

        square_box.pack_start(type_frame, False, False, 0)

        # Фрейм для автоматической генерации
        self.auto_frame = Gtk.Frame(label="Автоматическая генерация")
        auto_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.auto_frame.add(auto_box)

        # Параметры генерации
        params_grid = Gtk.Grid()
        params_grid.set_column_spacing(10)
        params_grid.set_row_spacing(10)
        params_grid.set_margin_top(10)
        params_grid.set_margin_bottom(10)
        params_grid.set_margin_start(10)
        params_grid.set_margin_end(10)
        auto_box.pack_start(params_grid, False, False, 0)

        # Размер квадрата
        size_label = Gtk.Label(label="Размер квадрата (N):")
        size_label.set_halign(Gtk.Align.START)
        params_grid.attach(size_label, 0, 0, 1, 1)

        self.size_adjustment = Gtk.Adjustment(
            value=5, lower=3, upper=15, step_increment=1
        )
        self.size_spin = Gtk.SpinButton(adjustment=self.size_adjustment)
        params_grid.attach(self.size_spin, 1, 0, 1, 1)

        # Метод генерации
        method_label = Gtk.Label(label="Метод генерации:")
        method_label.set_halign(Gtk.Align.START)
        params_grid.attach(method_label, 0, 1, 1, 1)

        self.method_combo = Gtk.ComboBoxText()
        for method in self.cipher.get_available_methods():
            self.method_combo.append_text(method)
        self.method_combo.set_active(0)
        self.method_combo.connect("changed", self.on_method_changed)
        params_grid.attach(self.method_combo, 1, 1, 1, 1)

        # Seed для случайной генерации
        seed_label = Gtk.Label(label="Seed (опционально):")
        seed_label.set_halign(Gtk.Align.START)
        params_grid.attach(seed_label, 0, 2, 1, 1)

        self.seed_entry = Gtk.Entry()
        self.seed_entry.set_placeholder_text("Оставьте пустым для случайного")
        self.seed_entry.set_width_chars(15)
        params_grid.attach(self.seed_entry, 1, 2, 1, 1)

        # Магическая сумма (для некоторых методов)
        self.magic_sum_label = Gtk.Label(label="Магическая сумма:")
        self.magic_sum_label.set_halign(Gtk.Align.START)
        params_grid.attach(self.magic_sum_label, 0, 3, 1, 1)

        self.magic_sum_adjustment = Gtk.Adjustment(
            value=65, lower=10, upper=10000, step_increment=1
        )
        self.magic_sum_spin = Gtk.SpinButton(adjustment=self.magic_sum_adjustment)
        self.magic_sum_spin.set_sensitive(False)
        params_grid.attach(self.magic_sum_spin, 1, 3, 1, 1)

        # Кнопки генерации
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        button_box.set_halign(Gtk.Align.CENTER)

        self.generate_btn = Gtk.Button(label="Сгенерировать квадрат")
        self.generate_btn.connect("clicked", self.on_generate_square_clicked)
        button_box.pack_start(self.generate_btn, False, False, 0)

        self.random_seed_btn = Gtk.Button(label="Случайный Seed")
        self.random_seed_btn.connect("clicked", self.on_random_seed_clicked)
        button_box.pack_start(self.random_seed_btn, False, False, 0)

        self.multiple_btn = Gtk.Button(label="Сгенерировать несколько")
        self.multiple_btn.connect("clicked", self.on_generate_multiple_clicked)
        button_box.pack_start(self.multiple_btn, False, False, 0)

        auto_box.pack_start(button_box, False, False, 0)

        square_box.pack_start(self.auto_frame, False, False, 0)

        # Фрейм для ручного ввода
        self.manual_frame = Gtk.Frame(label="Ручной ввод квадрата")
        self.manual_frame.set_visible(False)
        manual_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.manual_frame.add(manual_box)

        # Поле для ввода квадрата
        input_label = Gtk.Label(
            label="Введите квадрат (числа через пробел, строки через новую строку):"
        )
        input_label.set_halign(Gtk.Align.START)
        manual_box.pack_start(input_label, False, False, 0)

        self.square_input_scroll = Gtk.ScrolledWindow()
        self.square_input_scroll.set_hexpand(True)
        self.square_input_scroll.set_vexpand(True)
        self.square_input_scroll.set_min_content_height(150)

        self.square_input_text = Gtk.TextView()
        self.square_input_text.set_wrap_mode(Gtk.WrapMode.WORD)
        self.square_input_buffer = self.square_input_text.get_buffer()
        self.square_input_scroll.add(self.square_input_text)
        manual_box.pack_start(self.square_input_scroll, True, True, 0)

        # Кнопки для ручного ввода
        manual_btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        manual_btn_box.set_halign(Gtk.Align.CENTER)

        self.validate_btn = Gtk.Button(label="Проверить и использовать")
        self.validate_btn.connect("clicked", self.on_validate_square_clicked)
        manual_btn_box.pack_start(self.validate_btn, False, False, 0)

        self.clear_square_btn = Gtk.Button(label="Очистить")
        self.clear_square_btn.connect("clicked", self.on_clear_square_clicked)
        manual_btn_box.pack_start(self.clear_square_btn, False, False, 0)

        manual_box.pack_start(manual_btn_box, False, False, 0)

        square_box.pack_start(self.manual_frame, False, False, 0)

        # Область для отображения текущего квадрата
        display_frame = Gtk.Frame(label="Текущий магический квадрат")
        display_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        display_frame.add(display_box)

        self.square_display_scroll = Gtk.ScrolledWindow()
        self.square_display_scroll.set_hexpand(True)
        self.square_display_scroll.set_vexpand(True)
        self.square_display_scroll.set_min_content_height(250)

        self.square_display_text = Gtk.TextView()
        self.square_display_text.set_editable(False)
        self.square_display_text.set_monospace(True)
        self.square_display_buffer = self.square_display_text.get_buffer()
        self.square_display_scroll.add(self.square_display_text)
        display_box.pack_start(self.square_display_scroll, True, True, 0)

        # Информация о квадрате
        self.square_info_label = Gtk.Label(label="Квадрат не задан")
        self.square_info_label.set_halign(Gtk.Align.START)
        display_box.pack_start(self.square_info_label, False, False, 0)

        square_box.pack_start(display_frame, True, True, 0)

        # Добавляем вкладку в ноутбук
        self.notebook.append_page(square_box, Gtk.Label(label="Управление квадратом"))

    def create_encrypt_tab(self):
        """Создание вкладки шифрования"""
        encrypt_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        encrypt_box.set_margin_top(10)
        encrypt_box.set_margin_bottom(10)
        encrypt_box.set_margin_start(10)
        encrypt_box.set_margin_end(10)

        # Фрейм параметров
        params_frame = Gtk.Frame(label="Параметры")
        params_frame.set_margin_bottom(10)
        encrypt_box.pack_start(params_frame, False, False, 0)

        params_grid = Gtk.Grid()
        params_grid.set_column_spacing(10)
        params_grid.set_row_spacing(10)
        params_grid.set_margin_top(10)
        params_grid.set_margin_bottom(10)
        params_grid.set_margin_start(10)
        params_grid.set_margin_end(10)
        params_frame.add(params_grid)

        # Информация о текущем квадрате
        self.current_square_info = Gtk.Label(
            label="Используется автоматический квадрат 5x5"
        )
        self.current_square_info.set_halign(Gtk.Align.START)
        params_grid.attach(self.current_square_info, 0, 0, 3, 1)

        # Чекбокс использования подстановки
        self.use_substitution = Gtk.CheckButton(label="Использовать подстановку")
        params_grid.attach(self.use_substitution, 0, 1, 3, 1)

        # Горизонтальный бокс для текстовых областей
        text_panes = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        text_panes.set_position(450)
        encrypt_box.pack_start(text_panes, True, True, 0)

        # Левая панель - исходный текст
        input_frame = Gtk.Frame(label="Исходный текст")
        input_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        input_frame.add(input_box)

        self.input_scroll = Gtk.ScrolledWindow()
        self.input_scroll.set_hexpand(True)
        self.input_scroll.set_vexpand(True)
        self.input_scroll.set_min_content_height(200)

        self.input_text = Gtk.TextView()
        self.input_text.set_wrap_mode(Gtk.WrapMode.WORD)
        self.input_buffer = self.input_text.get_buffer()
        self.input_scroll.add(self.input_text)
        input_box.pack_start(self.input_scroll, True, True, 0)

        text_panes.add1(input_frame)

        # Правая панель - результат
        output_frame = Gtk.Frame(label="Результат")
        output_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        output_frame.add(output_box)

        self.output_scroll = Gtk.ScrolledWindow()
        self.output_scroll.set_hexpand(True)
        self.output_scroll.set_vexpand(True)
        self.output_scroll.set_min_content_height(200)

        self.output_text = Gtk.TextView()
        self.output_text.set_wrap_mode(Gtk.WrapMode.WORD)
        self.output_text.set_editable(False)
        self.output_buffer = self.output_text.get_buffer()
        self.output_scroll.add(self.output_text)
        output_box.pack_start(self.output_scroll, True, True, 0)

        text_panes.add2(output_frame)

        # Панель кнопок
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        button_box.set_halign(Gtk.Align.CENTER)
        button_box.set_margin_top(10)
        encrypt_box.pack_start(button_box, False, False, 0)

        # Кнопки
        self.encrypt_btn = Gtk.Button(label="Зашифровать")
        self.encrypt_btn.connect("clicked", self.on_encrypt_clicked)
        button_box.pack_start(self.encrypt_btn, False, False, 0)

        self.decrypt_btn = Gtk.Button(label="Расшифровать")
        self.decrypt_btn.connect("clicked", self.on_decrypt_clicked)
        button_box.pack_start(self.decrypt_btn, False, False, 0)

        self.clear_btn = Gtk.Button(label="Очистить")
        self.clear_btn.connect("clicked", self.on_clear_clicked)
        button_box.pack_start(self.clear_btn, False, False, 0)

        # Информационная панель
        info_frame = Gtk.Frame(label="Информация")
        info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        info_frame.add(info_box)

        self.info_label = Gtk.Label(label=".....")
        self.info_label.set_halign(Gtk.Align.START)
        self.info_label.set_margin_start(10)
        self.info_label.set_margin_top(5)
        self.info_label.set_margin_bottom(5)
        info_box.pack_start(self.info_label, True, True, 0)

        encrypt_box.pack_start(info_frame, False, False, 0)

        # Добавляем вкладку в ноутбук
        self.notebook.append_page(
            encrypt_box, Gtk.Label(label="Шифрование/Расшифрование")
        )

        # Инициализация текущего квадрата
        self.current_square = None
        self.current_n = 5
        self.is_custom_square = False
        self.current_method = "random"

    def on_method_changed(self, widget):
        """Обработчик изменения метода генерации"""
        method = widget.get_active_text()
        self.current_method = method

        # Активируем поле магической суммы для соответствующих методов
        if method in ["arithmetic", "geometric"]:
            self.magic_sum_spin.set_sensitive(True)
            # Устанавливаем классическую магическую сумму по умолчанию
            n = self.size_spin.get_value_as_int()
            classic_sum = n * (n * n + 1) // 2
            self.magic_sum_adjustment.set_value(classic_sum)

            # Предупреждение для geometric метода с четными размерами
            if method == "geometric" and n % 2 == 0:
                self.show_message(
                    "Информация",
                    "Для четных размеров geometric метод использует arithmetic метод",
                    Gtk.MessageType.INFO,
                )
        else:
            self.magic_sum_spin.set_sensitive(False)

    def on_validate_square_clicked(self, widget):
        """Проверка и использование введенного квадрата"""
        square_text = self.get_text_from_buffer(self.square_input_buffer)
        if not square_text.strip():
            self.show_message(
                "Ошибка", "Введите магический квадрат", Gtk.MessageType.ERROR
            )
            return

        try:
            # Парсинг введенного квадрата
            lines = square_text.strip().split("\n")
            n = len(lines)

            # Проверка на квадратную форму
            for i, line in enumerate(lines):
                row = line.strip().split()
                if len(row) != n:
                    raise ValueError(
                        f"Строка {i + 1} содержит {len(row)} элементов, ожидается {n}"
                    )

            # Создание матрицы
            square = np.zeros((n, n), dtype=int)
            for i, line in enumerate(lines):
                row = list(map(int, line.strip().split()))
                square[i] = row

            # Для пользовательских квадратов не проверяем уникальность чисел
            is_magic, message = self.cipher.validate_magic_square(
                square, check_uniqueness=False
            )

            if is_magic:
                self.current_square = square
                self.current_n = n
                self.is_custom_square = True
                self.update_square_display(square)

                magic_sum = self.cipher.calculate_magic_sum(square)
                self.update_square_info(f"Пользовательский квадрат {n}x{n}\n{message}")
                self.current_square_info.set_text(
                    f"Используется пользовательский квадрат {n}x{n} (сумма: {magic_sum})"
                )
                self.show_message(
                    "Успех",
                    f"Квадрат {n}x{n} корректен!\n{message}",
                    Gtk.MessageType.INFO,
                )
            else:
                self.show_message(
                    "Ошибка",
                    f"Квадрат не является магическим:\n{message}",
                    Gtk.MessageType.ERROR,
                )

        except ValueError as e:
            self.show_message(
                "Ошибка", f"Ошибка формата: {str(e)}", Gtk.MessageType.ERROR
            )
        except Exception as e:
            self.show_message(
                "Ошибка", f"Ошибка обработки: {str(e)}", Gtk.MessageType.ERROR
            )

    def on_square_type_changed(self, widget):
        """Обработчик изменения типа квадрата"""
        if widget.get_active_text() == "Ввести вручную":
            self.manual_frame.set_visible(True)
            self.auto_frame.set_visible(False)
        else:
            self.manual_frame.set_visible(False)
            self.auto_frame.set_visible(True)
            # Генерируем квадрат по умолчанию
            self.generate_default_square()

    def on_random_seed_clicked(self, widget):
        """Генерация случайного seed"""
        random_seed = random.randint(1, 1000000)
        self.seed_entry.set_text(str(random_seed))

    def generate_default_square(self):
        """Генерация квадрата по умолчанию"""
        n = self.size_spin.get_value_as_int()
        try:
            method = self.method_combo.get_active_text()
            seed_text = self.seed_entry.get_text().strip()
            seed = int(seed_text) if seed_text else None

            magic_sum = None
            if method in ["arithmetic", "geometric"]:
                magic_sum = int(self.magic_sum_spin.get_value())

            square = self.cipher.generate_magic_square(n, method, seed, magic_sum)
            self.current_square = square
            self.current_n = n
            self.is_custom_square = False
            self.update_square_display(square)

            magic_sum_actual = self.cipher.calculate_magic_sum(square)
            method_name = self.get_method_display_name(method)
            self.update_square_info(
                f"{method_name} квадрат {n}x{n}\nМагическая сумма: {magic_sum_actual}"
            )
            self.current_square_info.set_text(
                f"Используется {method_name} квадрат {n}x{n} (сумма: {magic_sum_actual})"
            )
        except Exception as e:
            self.show_message(
                "Ошибка", f"Ошибка генерации: {str(e)}", Gtk.MessageType.ERROR
            )

    def get_method_display_name(self, method: str) -> str:
        """Получить отображаемое имя метода"""
        names = {
            "random": "Случайный",
            "classic": "Классический",
            "arithmetic": "Арифметический",
            "geometric": "Геометрический",
        }
        return names.get(method, method)

    def on_generate_square_clicked(self, widget):
        """Обработчик кнопки генерации квадрата"""
        n = self.size_spin.get_value_as_int()
        try:
            method = self.method_combo.get_active_text()
            seed_text = self.seed_entry.get_text().strip()
            seed = int(seed_text) if seed_text else None

            magic_sum = None
            if method in ["arithmetic", "geometric"]:
                magic_sum = int(self.magic_sum_spin.get_value())

            square = self.cipher.generate_magic_square(n, method, seed, magic_sum)
            self.current_square = square
            self.current_n = n
            self.is_custom_square = False
            self.update_square_display(square)

            magic_sum_actual = self.cipher.calculate_magic_sum(square)
            method_name = self.get_method_display_name(method)
            self.update_square_info(
                f"{method_name} квадрат {n}x{n}\nМагическая сумма: {magic_sum_actual}"
            )
            self.current_square_info.set_text(
                f"Используется {method_name} квадрат {n}x{n} (сумма: {magic_sum_actual})"
            )

            self.show_message(
                "Успех",
                f"Квадрат {n}x{n} успешно сгенерирован\nМетод: {method_name}\nМагическая сумма: {magic_sum_actual}",
                Gtk.MessageType.INFO,
            )
        except Exception as e:
            self.show_message(
                "Ошибка", f"Ошибка генерации: {str(e)}", Gtk.MessageType.ERROR
            )

    def on_generate_multiple_clicked(self, widget):
        """Генерация нескольких квадратов для демонстрации"""
        n = self.size_spin.get_value_as_int()
        methods = self.cipher.get_available_methods()

        results = []
        for method in methods:
            try:
                if method in ["arithmetic", "geometric"]:
                    magic_sum = random.randint(50, 500)
                    square = self.cipher.generate_magic_square(
                        n, method, None, magic_sum
                    )
                else:
                    square = self.cipher.generate_magic_square(n, method)

                magic_sum_actual = self.cipher.calculate_magic_sum(square)
                results.append(
                    f"{self.get_method_display_name(method)}: сумма = {magic_sum_actual}"
                )
            except Exception:
                results.append(f"{self.get_method_display_name(method)}: ошибка")

        message = "Результаты генерации разных квадратов:\n" + "\n".join(results)
        self.show_message("Сравнение методов", message, Gtk.MessageType.INFO)

    def on_clear_square_clicked(self, widget):
        """Очистка поля ввода квадрата"""
        self.set_text_to_buffer(self.square_input_buffer, "")

    def update_square_display(self, square):
        """Обновление отображения квадрата"""
        n = square.shape[0]
        text = ""
        for i in range(n):
            row_text = " ".join(f"{square[i, j]:5d}" for j in range(n))
            text += row_text + "\n"

        # Добавляем информацию о магической сумме
        magic_sum = self.cipher.calculate_magic_sum(square)
        text += f"\nМагическая сумма: {magic_sum}"

        # Добавляем информацию о диапазоне значений
        min_val = np.min(square)
        max_val = np.max(square)
        text += f"\nДиапазон значений: {min_val} - {max_val}"

        self.set_text_to_buffer(self.square_display_buffer, text)

    def update_square_info(self, info):
        """Обновление информации о квадрате"""
        self.square_info_label.set_text(info)

    def get_text_from_buffer(self, buffer):
        """Получить текст из текстового буфера"""
        start_iter = buffer.get_start_iter()
        end_iter = buffer.get_end_iter()
        return buffer.get_text(start_iter, end_iter, False).strip()

    def set_text_to_buffer(self, buffer, text):
        """Установить текст в текстовый буфер"""
        buffer.set_text(text)

    def show_message(self, title, message, message_type=Gtk.MessageType.INFO):
        """Показать сообщение"""
        dialog = Gtk.MessageDialog(
            transient_for=self.window,
            flags=0,
            message_type=message_type,
            buttons=Gtk.ButtonsType.OK,
            text=title,
        )
        dialog.format_secondary_text(message)
        dialog.run()
        dialog.destroy()

    def on_encrypt_clicked(self, widget):
        """Обработчик кнопки шифрования"""
        if self.current_square is None:
            self.show_message(
                "Ошибка", "Сначала задайте магический квадрат", Gtk.MessageType.ERROR
            )
            return

        plaintext = self.get_text_from_buffer(self.input_buffer)
        if not plaintext:
            self.show_message(
                "Предупреждение",
                "Введите текст для шифрования",
                Gtk.MessageType.WARNING,
            )
            return

        thread = threading.Thread(target=self._encrypt_thread, args=(plaintext,))
        thread.daemon = True
        thread.start()

    def _encrypt_thread(self, plaintext):
        """Поток для шифрования"""
        try:
            use_sub = self.use_substitution.get_active()

            if self.is_custom_square:
                # Используем пользовательский квадрат
                encrypted = self.cipher.encrypt_with_square(
                    plaintext, self.current_square, use_sub
                )
            else:
                # Используем параметры генерации
                n = self.current_n
                method = self.method_combo.get_active_text()
                seed_text = self.seed_entry.get_text().strip()
                seed = int(seed_text) if seed_text else None

                magic_sum = None
                if method in ["arithmetic", "geometric"]:
                    magic_sum = int(self.magic_sum_spin.get_value())

                encrypted = self.cipher.encrypt(
                    plaintext, n, use_sub, method, seed, magic_sum
                )

            GLib.idle_add(
                self._update_output,
                encrypted,
                f"Текст зашифрован. Длина: {len(encrypted)} символов",
            )

        except Exception as e:
            error_msg = f"Ошибка при шифровании: {str(e)}"
            print(error_msg)
            print(traceback.format_exc())
            GLib.idle_add(
                self.show_message,
                "Ошибка",
                error_msg,
                Gtk.MessageType.ERROR,
            )

    def on_decrypt_clicked(self, widget):
        """Обработчик кнопки расшифрования"""
        if self.current_square is None:
            self.show_message(
                "Ошибка", "Сначала задайте магический квадрат", Gtk.MessageType.ERROR
            )
            return

        ciphertext = self.get_text_from_buffer(self.input_buffer)
        if not ciphertext:
            self.show_message(
                "Предупреждение",
                "Введите текст для расшифрования",
                Gtk.MessageType.WARNING,
            )
            return

        thread = threading.Thread(target=self._decrypt_thread, args=(ciphertext,))
        thread.daemon = True
        thread.start()

    def _decrypt_thread(self, ciphertext):
        """Поток для расшифрования"""
        try:
            use_sub = self.use_substitution.get_active()

            if self.is_custom_square:
                # Используем пользовательский квадрат
                decrypted = self.cipher.decrypt_with_square(
                    ciphertext, self.current_square, use_sub
                )
            else:
                # Используем параметры генерации
                n = self.current_n
                method = self.method_combo.get_active_text()
                seed_text = self.seed_entry.get_text().strip()
                seed = int(seed_text) if seed_text else None

                magic_sum = None
                if method in ["arithmetic", "geometric"]:
                    magic_sum = int(self.magic_sum_spin.get_value())

                decrypted = self.cipher.decrypt(
                    ciphertext, n, use_sub, method, seed, magic_sum
                )

            GLib.idle_add(
                self._update_output,
                decrypted,
                f"Текст расшифрован. Длина: {len(decrypted)} символов",
            )

        except Exception as e:
            error_msg = f"Ошибка при расшифровании: {str(e)}"
            print(error_msg)
            print(traceback.format_exc())
            GLib.idle_add(
                self.show_message,
                "Ошибка",
                error_msg,
                Gtk.MessageType.ERROR,
            )

    def _update_output(self, text, info_message):
        """Обновить вывод и информацию"""
        self.set_text_to_buffer(self.output_buffer, text)
        self.info_label.set_text(info_message)
        self.status_bar.push(self.status_context_id, info_message)

    def on_clear_clicked(self, widget):
        """Обработчик кнопки очистки"""
        self.set_text_to_buffer(self.input_buffer, "")
        self.set_text_to_buffer(self.output_buffer, "")
        self.info_label.set_text("Поля очищены")
        self.status_bar.push(self.status_context_id, "Поля очищены")

    def run(self):
        """Запуск приложения"""
        # Генерируем квадрат по умолчанию при запуске
        self.generate_default_square()
        self.window.show_all()
        Gtk.main()
