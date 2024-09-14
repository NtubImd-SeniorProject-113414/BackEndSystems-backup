import qrcode
from PIL import Image
from django.conf import settings
from django.templatetags.static import static
import os
import uuid

def generate_qr_code(data):
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=8,
            border=4,
        )

        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white').convert('RGB')

        logo_path = static('img/logo.png')

        logo_full_path = os.path.join(settings.BASE_DIR, logo_path)
        logo = Image.open(logo_full_path).convert("RGBA")

        logo_size = 50
        logo = logo.resize((logo_size, logo_size))

        logo_with_padding_size = int(logo_size)
        logo_with_padding = Image.new("RGB", (logo_with_padding_size, logo_with_padding_size), "white")

        logo_position_with_padding = (
            (logo_with_padding_size - logo_size) // 2,
            (logo_with_padding_size - logo_size) // 2
        )
        logo_with_padding.paste(logo, logo_position_with_padding, logo.split()[3])

        qr_width, qr_height = img.size
        logo_position = ((qr_width - logo_with_padding_size) // 2, (qr_height - logo_with_padding_size) // 2)

        img.paste(logo_with_padding, logo_position)

        file_name = f"{uuid.uuid4()}.png"
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)

        img.save(file_path)

        print(f"QR Code 已生成，並保存為 '{file_path}'")

        return file_path
    except:
        return None

