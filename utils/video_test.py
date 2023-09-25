from utils import webcam, make_video

for i in range(300):
    data = webcam.getFrame()
    print(i)

make_video.make_video('')
webcam.cleanup()
