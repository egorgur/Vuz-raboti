from docx import Document
import zipfile
import os
from PIL import Image, ImageOps
import numpy as np
import colorsys

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

def is_blue_dominant(rgb, threshold=30):
    """Проверяет, является ли синий доминирующим цветом"""
    r, g, b = rgb
    # Критерий 1: Синий канал значительно больше красного и зеленого
    blue_dominant = (b - r > threshold) and (b - g > threshold)
    
    # Критерий 2: Цвет в синей области HSV (200-260 градусов)
    h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
    h_degrees = h * 360
    in_blue_hue = 200 <= h_degrees <= 260
    
    return blue_dominant or in_blue_hue

def get_average_color(img):
    img_array = np.array(img)
    if img_array.ndim == 3 and img_array.shape[2] == 4:
        img_array = img_array[:, :, :3]
    if img_array.ndim == 3:
        avg_color = np.mean(img_array, axis=(0, 1))
    else:
        avg_color = [np.mean(img_array)] * 3
    return tuple(map(int, avg_color))

def process_docx_images(docx_path, output_path):
    temp_dir = "temp_docx_images"
    os.makedirs(temp_dir, exist_ok=True)

    with zipfile.ZipFile(docx_path, 'r') as zip_ref:
        image_files = [f for f in zip_ref.namelist() if f.startswith('word/media/')]
        if not image_files:
            print("В документе нет изображений!")
            return
        zip_ref.extractall(temp_dir, members=image_files)

    media_path = os.path.join(temp_dir, 'word/media')
    for img_file in os.listdir(media_path):
        img_path = os.path.join(media_path, img_file)
        try:
            with Image.open(img_path) as img:
                original_avg = get_average_color(img)
                hex_color = rgb_to_hex(original_avg)
                
                print(f"\nИзображение: {img_file}")
                print(f"Средний цвет: RGB {original_avg}, HEX {hex_color}")
                
                # Проверяем, нужно ли инвертировать это изображение
                if is_blue_dominant(original_avg):
                    print("🔵 Обнаружен синий доминирующий цвет - инвертируем")
                    if img.mode in ('RGBA', 'P', 'LA'):
                        img = img.convert('RGB')
                    inverted_img = ImageOps.invert(img)
                    inverted_img.save(img_path)
                    print("✅ Изображение инвертировано")
                else:
                    print("⚪ Белый/несиний цвет - пропускаем")
                    
        except Exception as e:
            print(f"❌ Ошибка: {str(e)}")

    with zipfile.ZipFile(docx_path, 'r') as original_zip:
        with zipfile.ZipFile(output_path, 'w') as new_zip:
            for file in original_zip.namelist():
                if file.startswith('word/media/'):
                    new_zip.write(os.path.join(temp_dir, file), file)
                else:
                    new_zip.writestr(file, original_zip.read(file))

    # Очистка
    for root, dirs, files in os.walk(temp_dir, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(temp_dir)
    print(f"\nГотово! Результат в {output_path}")

# Запуск
process_docx_images("input.docx", "output_filtered.docx")