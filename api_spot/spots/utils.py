from PIL import Image, ImageOps


def prepare_image(filepath: str, width: int, height: int) -> None:
    """Обработка изображения перед сохранением в базу данных"""
    img = Image.open(filepath)
    img = ImageOps.exif_transpose(img)
    new_image = img.resize((width, height))
    if new_image.format != "JPEG":
        new_image = new_image.convert("RGB")
    new_image.save(filepath, "JPEG")
