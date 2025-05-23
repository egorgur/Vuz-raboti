import pyclip
from PIL import Image
import io
import os
from datetime import datetime

def invert_image_from_clipboard():
    """Берет изображение из буфера, инвертирует и сохраняет"""
    try:
        # Получаем данные из буфера
        clipboard_data = pyclip.paste()
        if not clipboard_data:
            print("Буфер обмена пуст или не содержит изображение")
            return

        # Открываем изображение
        img = Image.open(io.BytesIO(clipboard_data))
        
        # Инвертируем цвета
        inverted_img = Image.eval(img, lambda x: 255 - x)
        
        # Создаем папку для результатов
        os.makedirs("inverted", exist_ok=True)
        
        # Генерируем имя файла с timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"inverted_{timestamp}.png"
        save_path = os.path.join("inverted", filename)
        
        # Сохраняем результат
        inverted_img.save(save_path)
        print(f"Инвертированное изображение сохранено: {os.path.abspath(save_path)}")
        
        # Показываем результат
        inverted_img.show()
        
    except Exception as e:
        print(f"Ошибка: {e}")

# Запускаем
if __name__ == "__main__":
    invert_image_from_clipboard()