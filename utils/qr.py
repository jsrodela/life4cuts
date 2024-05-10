import qrcode
from PIL.Image import Image
from main import settings

VIDEO_SERVER_URL = settings.VIDEO_SERVER_URL + '/receive?code='


def gen(code: int) -> Image:
    qrc = qrcode.QRCode(
        version=1,
        error_correction=qrcode.ERROR_CORRECT_M,
        box_size=3,
        border=1
    )
    qrc.add_data(VIDEO_SERVER_URL + str(code))
    img = qrc.make_image(back_color=(255, 255, 255), fill_color=(0, 0, 0))
    print("Generated qr code")
    return img.get_image()
