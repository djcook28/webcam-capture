import cv2
import time
import email

video = cv2.VideoCapture(0)
last_frame = None

# movement_list tracks whether there was or was not movement in the last 2 frames
movement_list = [False, False]

while True:
    # movement_detected checks if there was movement in the current frame
    movement_detected = False
    check, unmodified_frame = video.read()

    # changes the image from color to greyscale reducing the frame array
    current_frame = cv2.cvtColor(unmodified_frame, cv2.COLOR_BGR2GRAY)
    # blurs the frame array to better call out movement
    current_frame = cv2.GaussianBlur(current_frame, (21, 21), 0)

    if last_frame is None:
        last_frame = current_frame

    # computes the pixel differences between last and current frame
    delta_frame = cv2.absdiff(last_frame, current_frame)

    # magnifies pixel differences that are more white (>60) to max white
    thresh_frame = cv2.threshold(delta_frame, 45, 255, cv2.THRESH_BINARY)[1]

    # dilation helps to thicken the image filling in some of the black spaces
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

    # detects contours around the white area moving objects
    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # calculates the area of the white space contour and evaluates if it's too small to be an important object
        if cv2.contourArea(contour) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(unmodified_frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
        # if there was movement this frame, update movement_detected to True
        if rectangle.any():
            movement_detected = True

    # append latest frame movement detection to list, only retain last 2 values
    movement_list.append(movement_detected)
    movement_list = movement_list[-2:]

    # checks if the frame before had movement and this current frame does not.  If so we want to send an email with the last frame
    if(movement_list[0] == True and movement_list[1] == False):
        email.send_email(last_frame)

    cv2.imshow("My Video", unmodified_frame)

    key = cv2.waitKey(1)

    if key == ord("q"):
        break

    last_frame = current_frame

    time.sleep(1)

video.release()