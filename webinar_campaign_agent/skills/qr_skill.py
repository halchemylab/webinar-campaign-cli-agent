import urllib.parse

import qrcode

from .file_skill import OUTPUT_DIR, safe_filename, timestamped_filename


def generate_qr_code(url: str, filename: str = "campaign_qr.png") -> dict:
    """
    Creates a timestamped QR code PNG in output/.
    """
    safe_name = timestamped_filename(safe_filename(filename))

    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return {
            "status": "error",
            "message": "QR code URL must be a valid http or https URL.",
        }

    filepath = OUTPUT_DIR / safe_name

    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filepath)

    return {
        "status": "success",
        "path": str(filepath),
    }
