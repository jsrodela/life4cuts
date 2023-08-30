from PIL import Image

i = 2 #초록색 부분 제거단위 ( i by j 만큼  ( = 브러쉬 크기 ) )
j = 2

foreground_path = 'foreground.png'  #인물사진 ( with 크로마키 )
background_path = 'background.png'  #배경사진

foreground = Image.open(foreground_path).convert('RGBA')
background = Image.open(background_path).convert('RGBA')

width, height = 1080, 1080
foreground = foreground.resize((width, height))
background = background.resize((width, height))


def remove_green_background(image):
    pixels = image.load()
    for y in range(0, height, i):
        for x in range(0, width, j):
            r, g, b, a = pixels[x, y]
            if g - r > 20 and g - b > 20:
                for di in range(i + 1):
                    for dj in range(j + 1):
                        pixels[x - di , y - dj] = (r, g, b, 0)

remove_green_background(foreground)

composite = Image.alpha_composite(background, foreground)

composite.save('output.png')