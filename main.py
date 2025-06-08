import cv2
import time

video = cv2.VideoCapture(0)
last_frame = None

while True:
    check, current_frame = video.read()
    current_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    current_frame = cv2.GaussianBlur(current_frame, (21, 21), 0)

    if last_frame is None:
        last_frame = current_frame

    time.sleep(1)

    key = cv2.waitKey(1)

    delta_frame = cv2.absdiff(last_frame, current_frame)
    cv2.imshow("My Video", delta_frame)

    if key == ord("q"):
        break

    last_frame = current_frame
video.release()