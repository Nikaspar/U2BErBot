import json
import qrcode
import numpy as np
from qrcode.image.pil import PilImage
from PIL import Image, ImageDraw, ImageFont


def add_corners(img: PilImage, radius: int) -> PilImage:
    circle = Image.new('L', (radius * 2, radius * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, radius * 2 - 1, radius * 2 - 1), fill=255)
    alpha = Image.new('L', img.size, 255)
    w, h = img.size
    alpha.paste(circle.crop((0, 0, radius, radius)), (0, 0))
    alpha.paste(circle.crop((0, radius, radius, radius * 2)), (0, h - radius))
    alpha.paste(circle.crop((radius, 0, radius * 2, radius)), (w - radius, 0))
    alpha.paste(circle.crop((radius, radius, radius * 2, radius * 2)), (w - radius, h - radius))
    img.putalpha(alpha)
    return img


def get_addr(json_path: str, name: str) -> str | None:
    with open(json_path, 'r') as f:
        data = json.load(f)
        for d in data['wallets']:
            if d['name'] == name:
                return d['address']
        else:
            return None


def generate_qr(string: str,
                title: str,
                description: str = 'Send only $CRYPT to this address.',
                version: int = 1,
                box_size: int = 10,
                border: int = 2
                ) -> PilImage:
    description = description.replace('$CRYPT', title)
    qr = qrcode.QRCode(
            version=version,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=box_size,
            border=border,
        )
    qr.add_data(string)
    qr.make(fit=True)
    qr_code_img = qr.make_image()
    qr_code_img = qr_code_img.convert('RGBA')
    qr_code_img = add_corners(qr_code_img, 20)

    bg = np.zeros((440, 360))
    bg[:] = (40)
    bg_img = Image.fromarray(bg)
    bg_img = bg_img.convert('RGBA')
    bg_img.paste(qr_code_img, (15, 50), qr_code_img)

    txt_title = Image.new('RGBA', (360, 50), (0,0,0,0))
    d = ImageDraw.Draw(txt_title)
    fnt = ImageFont.truetype('fonts/UbuntuMono-Bold.ttf', 24)
    d.text((0, 0), title, font=fnt, fill=(149, 165, 187, 255))
    bg_img.paste(txt_title, (115, 14), txt_title)

    txt_desc = Image.new('RGBA', (360, 50), (0,0,0,0))
    d = ImageDraw.Draw(txt_desc)
    fnt = ImageFont.truetype('fonts/UbuntuMono-Regular.ttf', 14)
    d.text((0, 0), description, font=fnt, fill=(149, 165, 187, 255))
    bg_img.paste(txt_desc, (50, 395), txt_desc)

    bg_img = bg_img.convert('RGB')
    return bg_img
