from PIL import Image
import os

from utils import qr


def combine_photo(
        bg: str = "clientapp/static/images/2x3_white.png",
        pics: tuple = ("img_1.png", "img_2.png", "img_3.png", "img_4.png", "img_5.png", "img_6.png"),
        result: str = "result.png",
        qr_code: int = None
):
    background_path = os.path.join(os.getcwd(), bg)
    photo_path = []
    for i in range(6):
        photo_path.append(os.path.join(os.getcwd(), pics[i]))
    result_path = os.path.join(os.getcwd(), result)

    background = Image.open(background_path).convert("RGBA")
    photo = []
    for path in photo_path:
        photo.append(Image.open(path).convert("RGBA"))

    """
    middle_width = int(0.02 * background.size[0])
    middle_width2 = int(0.02 * background.size[0])
    left_margin = int(0.04 * background.size[0])
    right_margin = int(left_margin)
    photo_width = int(0.92 * background.size[0] / 3)

    photo_height = int(photo_width * photo[0].size[1] / photo[0].size[0])
    middle_height = int(0.02 * background.size[0])
    top_margin = int(0.05 * background.size[0])
    below_margin = int(background.size[1] - (photo_height*2 + middle_height + top_margin))
    """

    for i in range(6):
        # photo[i] = photo[i].resize((photo_width, photo_height))

        w = 523
        h = 400
        photo[i] = photo[i].resize((h*16//9, h))

        w_off = photo[i].width - w

        photo[i] = photo[i].crop((w_off//2, 0, photo[i].width - w_off//2, h))
        pass

    """
    pos1 = (75, 64, 596, 463)
    pos2 = (614, 64, 1136, 463)
    pos3 = (1154, 64, 1676, 463)
    pos4 = (75, 480, 596, 879)
    pos5 = (614, 480, 1136, 879)
    pos6 = (1154, 480, 1676, 879)
    """


    pos1 = (74, 64)
    pos2 = (614, 64)
    pos3 = (1154, 64)
    pos4 = (74, 480)
    pos5 = (614, 480)
    pos6 = (1154, 480)

    background.paste(photo[0], pos1)
    background.paste(photo[1], pos2)
    background.paste(photo[2], pos3)
    background.paste(photo[3], pos4)
    background.paste(photo[4], pos5)
    background.paste(photo[5], pos6)

    """
    background.paste(photo[0], (left_margin,top_margin))
    background.paste(photo[1], (left_margin+photo_width+middle_width,top_margin))
    background.paste(photo[2], (left_margin+photo_width*2+middle_width*2,top_margin))

    background.paste(photo[3], (left_margin,top_margin+photo_height+middle_height))
    background.paste(photo[4], (left_margin+photo_width+middle_width,top_margin+photo_height+middle_height))
    background.paste(photo[5], (left_margin+photo_width*2+middle_width*2,top_margin+photo_height+middle_height))
    """

    # (0, 0) ~ (92, 92)
    # x: 1584 ~ 1676, y: 989 ~ 1081
    if qr_code is not None:
        qr_img = qr.gen(qr_code)
        background.paste(qr_img, (1584, 989))

    background.save(result_path)
