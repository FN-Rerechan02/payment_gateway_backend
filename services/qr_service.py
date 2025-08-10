import os
from qr_generator import QRISGenerator
from app.config import settings
from uuid import uuid4

config = {
    'merchant_id': settings.merchant_id,
    'base_qr_string': settings.base_qr_string,
    'logo_path': settings.logo_path
}
qrgen = QRISGenerator(config)

# returns (qr_string, image_path)
def generate_qr_for_amount(amount: int, save_dir: str = "./qrs"):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir, exist_ok=True)

    qr_string = qrgen.generate_qr_string(amount)
    img = qrgen.generate_qr_with_logo(qr_string)
    filename = f"qris_{int(amount)}_{uuid4().hex}.png"
    path = os.path.join(save_dir, filename)
    img.save(path)
    return qr_string, path
