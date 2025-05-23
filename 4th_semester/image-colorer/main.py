import pyclip
from PIL import Image
import io
import os
from datetime import datetime

def invert_and_copy_image():
    """Берёт изображение из буфера, инвертирует, сохраняет и возвращает в буфер"""
    try:
        # 1. Получаем изображение из буфера
        clipboard_data = pyclip.paste()
        if not clipboard_data:
            print("Буфер обмена пуст или не содержит изображение")
            return False
        
        # 2. Открываем и инвертируем
        with Image.open(io.BytesIO(clipboard_data)) as img:
            # Инвертируем (с сохранением альфа-канала если есть)
            if img.mode == 'RGBA':
                r, g, b, a = img.split()
                rgb = Image.merge('RGB', (r, g, b))
                inverted = Image.eval(rgb, lambda x: 255 - x)
                r, g, b = inverted.split()
                inverted_img = Image.merge('RGBA', (r, g, b, a))
            else:
                inverted_img = Image.eval(img.convert('RGB'), lambda x: 255 - x)
            
            # 3. Сохраняем на диск
            os.makedirs("inverted", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = os.path.join("inverted", f"inverted_{timestamp}.png")
            inverted_img.save(save_path)
            print(f"✓ Сохранено: {os.path.abspath(save_path)}")
            
            # 4. Записываем в буфер обмена
            with io.BytesIO() as output:
                inverted_img.save(output, format="PNG")
                pyclip.copy(output.getvalue())
            print("✓ Инвертированное изображение скопировано в буфер обмена!")
            
            # 5. Показываем результат
            # inverted_img.show()
            return True
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

if __name__ == "__main__":
    print("🔁 Обработка изображения...")
    invert_and_copy_image()