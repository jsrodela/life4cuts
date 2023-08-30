from PIL import Image
import os


background_path = os.path.join(os.getcwd(),"잠신제 인생네컷","combine","background.png")
photo_path = [os.path.join(os.getcwd(),"잠신제 인생네컷","combine","photo"+str(num)+".png") for num in range(1,5)]
result_path = os.path.join(os.getcwd(),"잠신제 인생네컷","combine","result.png")

background = Image.open(background_path)
photo = []
for path in photo_path:
    photo.append(Image.open(path))

photo_width = int(0.4 * background.size[0])
middle_width = int(0.08 * background.size[0])
left_margin = int(0.06 * background.size[0])
right_margin = int(left_margin)

photo_height = int(0.4 * background.size[0])
middle_height = int(middle_width)
top_margin = int(left_margin)
below_margin = int(background.size[1] - (photo_height*2 + middle_height + top_margin))

for i in range(4):
    photo[i] = photo[i].resize((photo_width, photo_height))

background.paste(photo[0], (left_margin,top_margin))
background.paste(photo[1], (left_margin+photo_width+middle_width,top_margin))
background.paste(photo[2], (left_margin,top_margin+photo_height+middle_height))
background.paste(photo[3], (left_margin+photo_width+middle_width,top_margin+photo_height+middle_height))

background.save(result_path)