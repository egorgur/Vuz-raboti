import json
import gi
from rsa import RSAEncryption

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class RSAApp:
    def __init__(self):
        self.rsa = None
        self.encrypted_blocks = []
        self.public_key = {}

        # Создаем главное окно
        self.window = Gtk.Window(title="RSA Шифрование")
        self.window.set_default_size(800, 700)
        self.window.set_border_width(10)
        self.window.connect("destroy", Gtk.main_quit)

        # Главный контейнер
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.window.add(main_box)

        # Заголовок
        title_label = Gtk.Label()
        title_label.set_markup(
            "<span size='x-large' weight='bold'>RSA Шифрование</span>"
        )
        main_box.pack_start(title_label, False, False, 0)

        # Область для генерации ключей
        self.create_key_section(main_box)

        # Область для ввода текста
        self.create_text_section(main_box)

        # Область для результатов
        self.create_results_section(main_box)

        # Кнопки действий
        self.create_action_buttons(main_box)

        # Статус бар
        self.status_bar = Gtk.Statusbar()
        main_box.pack_start(self.status_bar, False, False, 0)

    def create_key_section(self, parent):
        frame = Gtk.Frame(label="Генерация ключей")
        frame.set_margin_top(10)
        parent.pack_start(frame, False, False, 0)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        box.set_border_width(10)
        frame.add(box)

        # Параметры
        params_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        box.pack_start(params_box, False, False, 0)

        digits_label = Gtk.Label(label="Количество цифр в модуле N:")
        params_box.pack_start(digits_label, False, False, 0)

        self.digits_entry = Gtk.Entry()
        self.digits_entry.set_text("31")
        self.digits_entry.set_width_chars(5)
        params_box.pack_start(self.digits_entry, False, False, 0)

        # Кнопка генерации ключей
        self.generate_btn = Gtk.Button(label="Сгенерировать ключи")
        self.generate_btn.connect("clicked", self.on_generate_keys)
        box.pack_start(self.generate_btn, False, False, 0)

        # Область для отображения ключей
        self.keys_text = Gtk.TextView()
        self.keys_text.set_editable(False)
        self.keys_text.set_wrap_mode(Gtk.WrapMode.WORD)

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_min_content_height(150)
        scrolled_window.add(self.keys_text)
        box.pack_start(scrolled_window, True, True, 0)

    def create_text_section(self, parent):
        notebook = Gtk.Notebook()
        notebook.set_margin_top(10)
        parent.pack_start(notebook, True, True, 0)

        # Вкладка исходного текста
        original_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        notebook.append_page(original_box, Gtk.Label(label="Исходный текст"))

        self.input_text = Gtk.TextView()
        self.input_text.set_wrap_mode(Gtk.WrapMode.WORD)

        scrolled_input = Gtk.ScrolledWindow()
        scrolled_input.set_min_content_height(200)
        scrolled_input.add(self.input_text)
        original_box.pack_start(scrolled_input, True, True, 0)

        # Вкладка зашифрованных блоков
        encrypted_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        notebook.append_page(encrypted_box, Gtk.Label(label="Зашифрованные блоки"))

        self.encrypted_text = Gtk.TextView()
        self.encrypted_text.set_editable(False)
        self.encrypted_text.set_wrap_mode(Gtk.WrapMode.WORD)

        scrolled_encrypted = Gtk.ScrolledWindow()
        scrolled_encrypted.set_min_content_height(200)
        scrolled_encrypted.add(self.encrypted_text)
        encrypted_box.pack_start(scrolled_encrypted, True, True, 0)

        # Вкладка результатов
        result_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        notebook.append_page(result_box, Gtk.Label(label="Результат"))

        self.result_text = Gtk.TextView()
        self.result_text.set_editable(False)
        self.result_text.set_wrap_mode(Gtk.WrapMode.WORD)

        scrolled_result = Gtk.ScrolledWindow()
        scrolled_result.set_min_content_height(200)
        scrolled_result.add(self.result_text)
        result_box.pack_start(scrolled_result, True, True, 0)

    def create_results_section(self, parent):
        frame = Gtk.Frame(label="Информация о шифровании")
        parent.pack_start(frame, False, False, 0)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        box.set_border_width(10)
        frame.add(box)

        self.info_text = Gtk.TextView()
        self.info_text.set_editable(False)
        self.info_text.set_wrap_mode(Gtk.WrapMode.WORD)

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_min_content_height(100)
        scrolled_window.add(self.info_text)
        box.pack_start(scrolled_window, True, True, 0)

    def create_action_buttons(self, parent):
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        button_box.set_halign(Gtk.Align.CENTER)
        button_box.set_margin_top(10)
        parent.pack_start(button_box, False, False, 0)

        self.encrypt_btn = Gtk.Button(label="Зашифровать")
        self.encrypt_btn.connect("clicked", self.on_encrypt)
        self.encrypt_btn.set_sensitive(False)
        button_box.pack_start(self.encrypt_btn, False, False, 0)

        self.decrypt_btn = Gtk.Button(label="Расшифровать")
        self.decrypt_btn.connect("clicked", self.on_decrypt)
        self.decrypt_btn.set_sensitive(False)
        button_box.pack_start(self.decrypt_btn, False, False, 0)

        clear_btn = Gtk.Button(label="Очистить все")
        clear_btn.connect("clicked", self.on_clear)
        button_box.pack_start(clear_btn, False, False, 0)

    def update_status(self, message):
        context_id = self.status_bar.get_context_id("status")
        self.status_bar.push(context_id, message)

    def get_buffer_text(self, text_view):
        """Безопасное получение текста из TextView"""
        buffer = text_view.get_buffer()
        start_iter = buffer.get_start_iter()
        end_iter = buffer.get_end_iter()
        text = buffer.get_text(start_iter, end_iter, True)
        return text if text is not None else ""

    def on_generate_keys(self, widget):
        try:
            n_digits = int(self.digits_entry.get_text())
            if n_digits < 10:
                self.show_error("Количество цифр должно быть не менее 10")
                return

            self.update_status("Генерация ключей...")

            # Генерация RSA ключей
            self.rsa = RSAEncryption(n_digits)
            key_info = self.rsa.get_key_info()

            # Отображение информации о ключах
            keys_buffer = self.keys_text.get_buffer()
            keys_text = f"""P: {key_info["p"]}

Q: {key_info["q"]}

Модуль N: {key_info["n"]}
Длина N: {key_info["n_digits"]} цифр

φ(N): {key_info["phi"]}

Открытая экспонента e: {key_info["public_exponent"]}

Закрытая экспонента d: {key_info["private_exponent"]}

Размер блока: {key_info["block_size_bytes"]} байт"""

            keys_buffer.set_text(keys_text)

            # Активируем кнопки
            self.encrypt_btn.set_sensitive(True)
            self.decrypt_btn.set_sensitive(True)

            self.update_status("Ключи успешно сгенерированы")

        except ValueError:
            self.show_error("Введите корректное число цифр")
        except Exception as e:
            self.show_error(f"Ошибка при генерации ключей: {str(e)}")

    def on_encrypt(self, widget):
        if not self.rsa:
            self.show_error("Сначала сгенерируйте ключи")
            return

        try:
            # Получаем исходный текст
            plaintext = self.get_buffer_text(self.input_text)

            if not plaintext.strip():
                self.show_error("Введите текст для шифрования")
                return

            self.update_status("Шифрование...")

            # Шифруем текст
            self.encrypted_blocks, self.public_key = self.rsa.encrypt(plaintext)

            # Отображаем зашифрованные блоки
            encrypted_buffer = self.encrypted_text.get_buffer()
            encrypted_text = json.dumps(self.encrypted_blocks)
            encrypted_buffer.set_text(encrypted_text)

            # Обновляем информацию
            info_buffer = self.info_text.get_buffer()
            info_text = f"""Текст успешно зашифрован!
Количество блоков: {len(self.encrypted_blocks)}
Размер исходного текста: {len(plaintext)} символов
Открытый ключ: (e={self.public_key["e"]}, n={self.public_key["n"]})"""

            info_buffer.set_text(info_text)
            self.update_status("Текст успешно зашифрован")

        except Exception as e:
            self.show_error(f"Ошибка при шифровании: {str(e)}")

    def on_decrypt(self, widget):
        if not self.rsa:
            self.show_error("Сначала сгенерируйте ключи")
            return

        try:
            # Получаем зашифрованные блоки
            encrypted_text = self.get_buffer_text(self.encrypted_text)

            if not encrypted_text.strip():
                self.show_error("Нет данных для расшифровки")
                return

            self.update_status("Расшифровка...")

            # Парсим блоки
            encrypted_blocks = json.loads(encrypted_text)

            # Расшифровываем
            decrypted_text = self.rsa.decrypt(encrypted_blocks)

            # Отображаем результат
            result_buffer = self.result_text.get_buffer()
            result_buffer.set_text(decrypted_text)

            # Обновляем информацию
            info_buffer = self.info_text.get_buffer()
            info_text = f"""Текст успешно расшифрован!
Длина текста: {len(decrypted_text)} символов
Количество блоков: {len(encrypted_blocks)}"""

            info_buffer.set_text(info_text)
            self.update_status("Текст успешно расшифрован")

        except json.JSONDecodeError:
            self.show_error("Неверный формат зашифрованных блоков")
        except Exception as e:
            self.show_error(f"Ошибка при расшифровке: {str(e)}")

    def on_test(self, widget):
        """Тестовый пример"""
        test_text = """Привет! Hello! 12345 
Тестовое сообщение на русском и английском.
Test message in Russian and English!"""

        input_buffer = self.input_text.get_buffer()
        input_buffer.set_text(test_text)
        self.update_status("Загружен тестовый пример")

    def on_clear(self, widget):
        # Очищаем все текстовые поля
        self.keys_text.get_buffer().set_text("")
        self.input_text.get_buffer().set_text("")
        self.encrypted_text.get_buffer().set_text("")
        self.result_text.get_buffer().set_text("")
        self.info_text.get_buffer().set_text("")

        # Деактивируем кнопки
        self.encrypt_btn.set_sensitive(False)
        self.decrypt_btn.set_sensitive(False)

        self.rsa = None
        self.encrypted_blocks = []
        self.public_key = {}

        self.update_status("Все поля очищены")

    def show_error(self, message):
        dialog = Gtk.MessageDialog(
            transient_for=self.window,
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text=message,
        )
        dialog.run()
        dialog.destroy()
        self.update_status(f"Ошибка: {message}")

    def run(self):
        self.window.show_all()
        self.update_status("Готов к работе")
        Gtk.main()


if __name__ == "__main__":
    app = RSAApp()
    app.run()
