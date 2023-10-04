from PIL import Image, ImageOps


def prepare_image(image, filepath: str) -> None:
    """Обработка изображения перед сохранением в базу данных"""
    img = Image.open(image)
    fixed_width = 1080
    img = Image.open(filepath)
    img = ImageOps.exif_transpose(img)
    width_percent = fixed_width / float(img.size[0])
    height_size = int((float(img.size[1]) * float(width_percent)))
    new_image = img.resize((fixed_width, height_size))
    if new_image.format != "JPEG":
        new_image = new_image.convert("RGB")
    new_image.save(filepath, "JPEG")
