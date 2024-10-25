import base64
from io import BytesIO

from PIL import Image


def base64_to_image_with_format(base64_str, output_file_path, format="PNG"):
    image_data = base64.b64decode(base64_str)

    image = Image.open(BytesIO(image_data))
    image.save(output_file_path, format=format)
