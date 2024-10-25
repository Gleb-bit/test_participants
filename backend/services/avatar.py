from PIL import Image


def add_watermark(
    input_image_path: str,
    watermark_path: str,
    output_image_path: str,
    transparency: float = 130,
):
    avatar = Image.open(input_image_path).convert("RGBA")
    watermark = Image.open(watermark_path).convert("RGBA")

    watermark_size = (int(avatar.size[0] * 0.2), int(avatar.size[1] * 0.2))
    watermark = watermark.resize(watermark_size, Image.Resampling.LANCZOS)

    alpha = watermark.split()[3]
    alpha = alpha.point(lambda p: p * (transparency / 255.0))
    watermark.putalpha(alpha)

    position = (0, avatar.size[1] - watermark.size[1])

    combined = Image.new("RGBA", avatar.size)
    combined.paste(avatar, (0, 0))
    combined.paste(watermark, position, mask=watermark)

    combined.save(output_image_path, "PNG")

    return output_image_path
