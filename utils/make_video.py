import cv2
import os
import numpy as np

frames = []
# image_folder = os.path.join(os.getcwd(), "잠신제 인생네컷", "images")


def make_video(output_path: str):
    global frames
    # video_name = 'video.avi'

    """
    images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
    print(os.path.join(image_folder, images[0]))

    frame = np.fromfile(os.path.join(image_folder, images[0]), np.uint8)
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    height, width, layers = frame.shape
    """

    images = np.array(frames)
    height, width, layers = images[0].shape

    video = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'DIVX'), 30, (width, height))
    for image in images:
        # frame = np.fromfile(os.path.join(image_folder, image), np.uint8)
        # video.write(cv2.imdecode(image, cv2.IMREAD_COLOR))
        video.write(image)

    # cv2.destroyAllWindows()
    video.release()
    frames.clear()
    print("Video complete")
