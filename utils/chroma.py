from PIL import Image, ImageFilter, ImageEnhance

from clientapp import static

i = 1  # 초록색 부분 제거단위 ( i by j 만큼  ( = 브러쉬 크기 ) )
j = 1
# 2

"""
foreground_path = 'foreground.png'  #인물사진 ( with 크로마키 )
background_path = 'background.png'  #배경사진

foreground = Image.open(foreground_path).convert('RGBA')
background = Image.open(background_path).convert('RGBA')

foreground = foreground.resize((width, height))
background = background.resize((width, height))
"""


# width, height = 1920, 1080


def remove_green_background(image_path, bg_path):
    # 전반적으로 초록 낮추기 (빨강은 보정)
    image = Image.open(image_path).convert('RGB', (
        0.95, 0, 0, 0,
        0, 0.9, 0, 0,
        0, 0, 1, 0
    )).convert('RGBA')

    image = brightness(image)  # 밝기 보정

    # 크로마키 위해 픽셀 배열로 변환
    pixels = image.load()
    for y in range(0, image.height, i):
        for x in range(0, image.width, j):

            r, g, b, a = pixels[x, y]
            NUM = 25  # 20

            # 첫번째는 보통 초록 배경 지우기, 두번째는 조명땜에 밝아진 초록 배경 지우기
            # 세번째는 선글라스 때문에 어두워진 초록 배경 지우기
            if (g - r > NUM and g - b > NUM) or (g >= 250 and (g - r > NUM)) or (g >= 150 and (g - r > 100)):
                for di in range(i + 1):
                    for dj in range(j + 1):
                        pixels[x - di, y - dj] = (r, g, b, 0)
    # image = image.filter(ImageFilter.DETAIL).filter(ImageFilter.SHARPEN)

    background = Image.open(bg_path).convert('RGBA').resize(image.size, Image.LANCZOS)
    composite = Image.alpha_composite(background, image)
    return composite
    # return pixels


def brightness(image):
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(1.1)


if __name__ == '__main__':
    remove_green_background('../test_input2.png', '../bg1.jpg').save('../output.png')

"""
remove_green_background(foreground)

composite = Image.alpha_composite(background, foreground)

composite.save('output.png')
"""
