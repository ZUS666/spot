from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage as storage 
from django.core.files import File
from pathlib import Path
from PIL import Image
from io import BytesIO


def image_resize(image, width, height):
    image_types = {
        "jpg": "JPEG",
        "jpeg": "JPEG",
        "png": "PNG",
        "gif": "GIF",
        "tif": "TIFF",
        "tiff": "TIFF",
    }
    img = Image.open(image)
    if img.width > width or img.height > height:
        img.thumbnail((width, height))
        img_filename = Path(image.file.name).name
        img_suffix = Path(image.file.name).name.split(".")[-1]
        img_format = image_types[img_suffix]
        buffer = BytesIO()
        img.save(buffer, format=img_format)
        print(img.width, img.height)
        file_object = ContentFile(buffer.getvalue())
        image.save(img_filename, file_object)
