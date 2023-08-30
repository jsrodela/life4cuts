import cv2
import os
import numpy as np


image_folder = os.path.join(os.getcwd(),"잠신제 인생네컷","images")
video_name = 'video.avi'

images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
print(os.path.join(image_folder, images[0]))

frame = np.fromfile(os.path.join(image_folder, images[0]), np.uint8)
frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
height, width, layers = frame.shape

video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'DIVX'), 100, (width, height))

for image in images:
    frame = np.fromfile(os.path.join(image_folder, image), np.uint8)
    video.write(cv2.imdecode(frame, cv2.IMREAD_COLOR))

cv2.destroyAllWindows()
video.release()