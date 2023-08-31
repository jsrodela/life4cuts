from PIL import Image
import os


def combine_photo():
    background_path = os.path.join(os.getcwd(),"clientapp","static","images","2x3_white.png")
    photo_path = [os.path.join(os.getcwd(),"img_"+str(num)+".png") for num in range(1,7)]
    result_path = os.path.join(os.getcwd(),"result.png")

    background = Image.open(background_path)
    photo = []
    for path in photo_path:
        photo.append(Image.open(path))

    middle_width = int(0.02 * background.size[0])
    middle_width2 = int(0.02 * background.size[0])
    left_margin = int(0.04 * background.size[0])
    right_margin = int(left_margin)
    photo_width = int(0.92 * background.size[0] / 3)

    photo_height = int(photo_width * photo[0].size[1] / photo[0].size[0])
    middle_height = int(0.02 * background.size[0])
    top_margin = int(0.05 * background.size[0])
    below_margin = int(background.size[1] - (photo_height*2 + middle_height + top_margin))

    for i in range(4):
        photo[i] = photo[i].resize((photo_width, photo_height))

    background.paste(photo[0], (left_margin,top_margin))
    background.paste(photo[1], (left_margin+photo_width+middle_width,top_margin))
    background.paste(photo[2], (left_margin+photo_width*2+middle_width*2,top_margin))

    background.paste(photo[3], (left_margin,top_margin+photo_height+middle_height))
    background.paste(photo[4], (left_margin+photo_width+middle_width,top_margin+photo_height+middle_height))
    background.paste(photo[5], (left_margin+photo_width*2+middle_width*2,top_margin+photo_height+middle_height))

    background.save(result_path)