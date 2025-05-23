from docx import Document
import zipfile
import os
from PIL import Image, ImageOps

def invert_images_in_docx(docx_path, output_path):
    temp_dir = "temp_docx_images"
    os.makedirs(temp_dir, exist_ok=True)

    # Шаг 1: Извлекаем изображения из .docx
    with zipfile.ZipFile(docx_path, 'r') as zip_ref:
        image_files = [f for f in zip_ref.namelist() if f.startswith('word/media/')]
        if not image_files:
            print("В документе нет изображений!")
            return
        zip_ref.extractall(temp_dir, members=image_files)

    # Шаг 2: Инвертируем каждое изображение
    media_path = os.path.join(temp_dir, 'word/media')
    for img_file in os.listdir(media_path):
        img_path = os.path.join(media_path, img_file)
        try:
            with Image.open(img_path) as img:
                # Конвертируем в RGB, если нужно
                if img.mode in ('RGBA', 'P', 'LA'):
                    img = img.convert('RGB')
                inverted_img = ImageOps.invert(img)
                inverted_img.save(img_path)
                print(f"Изображение {img_file} инвертировано.")
        except Exception as e:
            print(f"Ошибка при обработке {img_file}: {str(e)}")

    # Шаг 3: Перепаковываем .docx с новыми изображениями
    with zipfile.ZipFile(docx_path, 'r') as original_zip:
        with zipfile.ZipFile(output_path, 'w') as new_zip:
            for file in original_zip.namelist():
                if file.startswith('word/media/'):
                    # Заменяем старые изображения новыми
                    new_zip.write(os.path.join(temp_dir, file), file)
                else:
                    # Копируем остальные файлы без изменений
                    new_zip.writestr(file, original_zip.read(file))

    # Очистка
    for root, dirs, files in os.walk(temp_dir, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(temp_dir)
    print(f"Готово! Инвертированный документ: {output_path}")

# Пример использования
invert_images_in_docx("input.docx", "output_inverted.docx")