import os

from PIL import Image

from utils import combine_photo, chroma

cwd = os.path.join(os.getcwd(), input('작업 폴더 경로 (life4cuts/...):'))
output_name = input('출력 파일 이름:')
bg = input('배경 번호:')
frame = input('프레임 번호:')
images = []
for i in range(1, 7):
    images.append(input('%d번째 사진 파일: ' % i))

for img in images:
    chroma.remove_green_background(Image.open(img), '').save('../output.png')
    os.rename('../output.png', cwd % img)

combine_photo.combine_photo()
