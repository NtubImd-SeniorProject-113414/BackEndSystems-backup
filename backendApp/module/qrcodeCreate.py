import qrcode
from PIL import Image
from django.conf import settings
import os
import uuid

def generate_qr_code(data):
    if not data:
        raise ValueError("Data for QR Code cannot be empty")

    print(f"Generating QR code with data: {data}")  # 调试输出

    # 创建二维码
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,  # 调大 box_size
        border=5,     # 调大 border
    )

    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white').convert('RGB')

    logo_full_path = os.path.join(settings.STATICFILES_DIRS[0], 'img', 'logo.png')

    if not os.path.exists(logo_full_path):
        raise FileNotFoundError(f"Logo file not found at {logo_full_path}")

    logo = Image.open(logo_full_path).convert("RGBA")
    logo_size = 50  # 控制 logo 大小，确保不会过度覆盖二维码
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
    relative_file_path = os.path.join(settings.MEDIA_URL, file_name)
    
    return relative_file_path
