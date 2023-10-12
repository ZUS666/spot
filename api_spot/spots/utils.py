from PIL import Image, ImageOps

from spots.constants import SMALL_HEIGHT, SMALL_WIDTH


def prepare_image(filepath):
    """Обработка изображения перед сохранением в базу данных"""
    img = Image.open(filepath)
    img = ImageOps.exif_transpose(img)
    new_image = img.resize((SMALL_WIDTH, SMALL_HEIGHT))
    if new_image.format != "JPEG":
        new_image = new_image.convert("RGB")
    new_image.save(filepath, "JPEG")
