import time
import cv2

capture = cv2.VideoCapture(2, cv2.CAP_DSHOW)
print(capture.get(3), capture.get(4))

# capture.read()
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
# capture.set(cv2.CAP_PROP_POS_FRAMES, 60)

capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))


print(capture.get(3), capture.get(4))


prevTime = 0
while cv2.waitKey(33) < 0:
    ret, frame = capture.read()

    ########### 추가 ##################
    # 현재 시간 가져오기 (초단위로 가져옴)
    curTime = time.time()

    # 현재 시간에서 이전 시간을 빼면?
    # 한번 돌아온 시간!!
    sec = curTime - prevTime
    # 이전 시간을 현재시간으로 다시 저장시킴
    prevTime = curTime

    # 프레임 계산 한바퀴 돌아온 시간을 1초로 나누면 된다.
    # 1 / time per frame
    fps = 1 / (sec)

    # 디버그 메시지로 확인해보기
    print(
    "Time {0} ".format(sec))
    print ("Estimated fps {0} ".format(fps))

    # 프레임 수를 문자열에 저장
    str = "FPS : %0.1f" % fps

    # 표시
    cv2.putText(frame, str, (0, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))
    ###################################

    cv2.imshow("VideoFrame", frame)

capture.release()
cv2.destroyAllWindows()