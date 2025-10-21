import trace
from cipher import MagicSquareCipher
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib
import numpy as np
import threading


class CipherGUI:
    """Графический интерфейс для шифровальщика на GTK"""

    def __init__(self, cipher: MagicSquareCipher):
        self.cipher = cipher
        self.setup_theme()
        self.create_ui()
    
    def setup_theme(self):
        """Настройка темы в соответствии с системой"""
        # Получаем настройки по умолчанию
        settings = Gtk.Settings.get_default()
        
        # Автоматическое определение системной темы
        self.detect_system_theme()
        
        # Настройка дополнительных параметров
        settings.set_property("gtk-application-prefer-dark-theme", self.prefers_dark)
        
    def detect_system_theme(self):
        """Определение системной темы"""
        settings = Gtk.Settings.get_default()
        
        # Получаем текущую тему
        current_theme = settings.get_property("gtk-theme-name")
        print(f"Текущая тема GTK: {current_theme}")
        
        # Проверяем предпочтение темной темы
        self.prefers_dark = settings.get_property("gtk-application-prefer-dark-theme")
        
        # Альтернативный способ через GdkDisplay
        display = Gdk.Display.get_default()
        if display:
            # Проверяем поддержку темной темы
            app = Gtk.Application.get_default()
            if app:
                app.prefers_color_scheme = Gtk.SettingsColorScheme.PREFER_DARK if self.prefers_dark else Gtk.SettingsColorScheme.PREFER_LIGHT
                

    def create_ui(self):
        """Создание пользовательского интерфейса"""
        # Главное окно
        self.window = Gtk.Window(title="Шифр на основе магических квадратов")
        self.window.set_default_size(900, 700)
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

        # Статусная строка
        self.status_bar = Gtk.Statusbar()
        self.status_context_id = self.status_bar.get_context_id("main")
        main_box.pack_start(self.status_bar, False, False, 0)

        self.window.show_all()

    def create_encrypt_tab(self):
        """Создание вкладки шифрования"""
        # Основной контейнер вкладки
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

        # Размер квадрата
        size_label = Gtk.Label(label="Размер квадрата (N):")
        size_label.set_halign(Gtk.Align.START)
        params_grid.attach(size_label, 0, 0, 1, 1)

        self.size_adjustment = Gtk.Adjustment(
            value=5, lower=3, upper=10, step_increment=1
        )
        self.size_spin = Gtk.SpinButton(adjustment=self.size_adjustment)
        params_grid.attach(self.size_spin, 1, 0, 1, 1)

        # Ключ подстановки
        # key_label = Gtk.Label(label="Ключ подстановки:")
        # key_label.set_halign(Gtk.Align.START)
        # params_grid.attach(key_label, 2, 0, 1, 1)

        # self.key_entry = Gtk.Entry()
        # self.key_entry.set_width_chars(20)
        # params_grid.attach(self.key_entry, 3, 0, 1, 1)

        # Чекбокс использования подстановки
        self.use_substitution = Gtk.CheckButton(label="Использовать подстановку")
        params_grid.attach(self.use_substitution, 4, 0, 1, 1)

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

        self.square_btn = Gtk.Button(label="Показать квадрат")
        self.square_btn.connect("clicked", self.on_show_square_clicked)
        button_box.pack_start(self.square_btn, False, False, 0)

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
        plaintext = self.get_text_from_buffer(self.input_buffer)
        if not plaintext:
            self.show_message(
                "Предупреждение",
                "Введите текст для шифрования",
                Gtk.MessageType.WARNING,
            )
            return

        # Запускаем в отдельном потоке, чтобы не блокировать UI
        thread = threading.Thread(target=self._encrypt_thread, args=(plaintext,))
        thread.daemon = True
        thread.start()

    def _encrypt_thread(self, plaintext):
        """Поток для шифрования"""
        # try:
        n = self.size_spin.get_value_as_int()
        use_sub = self.use_substitution.get_active()

        encrypted = self.cipher.encrypt(plaintext, n, use_sub)

        # Обновляем UI в главном потоке
        GLib.idle_add(
            self._update_output,
            encrypted,
            f"Текст зашифрован. Длина: {len(encrypted)} символов",
        )

        # except Exception as e:
        #     print(e)
        #     print(trace.)
        #     GLib.idle_add(
        #         self.show_message,
        #         "Ошибка",
        #         f"Ошибка при шифровании: {str(e)}",
        #         Gtk.MessageType.ERROR,
        #     )

    def on_decrypt_clicked(self, widget):
        """Обработчик кнопки расшифрования"""
        ciphertext = self.get_text_from_buffer(self.input_buffer)
        if not ciphertext:
            self.show_message(
                "Предупреждение",
                "Введите текст для расшифрования",
                Gtk.MessageType.WARNING,
            )
            return

        # Запускаем в отдельном потоке
        thread = threading.Thread(target=self._decrypt_thread, args=(ciphertext,))
        thread.daemon = True
        thread.start()

    def _decrypt_thread(self, ciphertext):
        """Поток для расшифрования"""
        # try:
        n = self.size_spin.get_value_as_int()
        use_sub = self.use_substitution.get_active()

        decrypted = self.cipher.decrypt(ciphertext, n, use_sub)

        # Обновляем UI в главном потоке
        GLib.idle_add(
            self._update_output,
            decrypted,
            f"Текст расшифрован. Длина: {len(decrypted)} символов",
        )

        # except Exception as e:
        #     print(e)
        #     GLib.idle_add(
        #         self.show_message,
        #         "Ошибка",
        #         f"Ошибка при расшифровании: {str(e)}",
        #         Gtk.MessageType.ERROR,
        #     )

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

    def on_show_square_clicked(self, widget):
        """Показать магический квадрат"""
        try:
            n = self.size_spin.get_value_as_int()
            square = self.cipher.generate_magic_square(n)

            # Создание окна для отображения квадрата
            square_window = Gtk.Window(title=f"Магический квадрат {n}x{n}")
            square_window.set_default_size(300, 300)
            square_window.set_transient_for(self.window)
            square_window.set_modal(True)

            # Основной контейнер
            main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
            main_box.set_margin_top(10)
            main_box.set_margin_bottom(10)
            main_box.set_margin_start(10)
            main_box.set_margin_end(10)
            square_window.add(main_box)

            # Текстовое поле для отображения квадрата
            scroll = Gtk.ScrolledWindow()
            scroll.set_hexpand(True)
            scroll.set_vexpand(True)
            main_box.pack_start(scroll, True, True, 0)

            text_view = Gtk.TextView()
            text_view.set_editable(False)
            text_view.set_monospace(True)
            text_buffer = text_view.get_buffer()
            scroll.add(text_view)

            # Формирование текста
            text = ""
            for i in range(n):
                row_text = " ".join(f"{square[i, j]:3d}" for j in range(n))
                text += row_text + "\n"

            # Проверка магической суммы
            magic_sum = np.sum(square[0, :])
            text += f"\nМагическая сумма: {magic_sum}"

            text_buffer.set_text(text)

            # Кнопка закрытия
            close_btn = Gtk.Button(label="Закрыть")
            close_btn.connect("clicked", lambda w: square_window.destroy())
            main_box.pack_start(close_btn, False, False, 0)

            square_window.show_all()

        except Exception as e:
            self.show_message(
                "Ошибка",
                f"Ошибка при создании квадрата: {str(e)}",
                Gtk.MessageType.ERROR,
            )

    def run(self):
        """Запуск приложения"""
        self.window.show_all()
        Gtk.main()
