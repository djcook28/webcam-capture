import cv2

def simplify_frame(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # blurs the frame array to better call out movement
    frame = cv2.GaussianBlur(frame, (21, 21), 0)
    return frame

def frame_compare(last_frame, current_frame, unmodified_frame):
    movement_detected = False
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
        rectangle = cv2.rectangle(unmodified_frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        # if there was movement this frame, update movement_detected to True
        if rectangle.any():
            movement_detected = True
    return movement_detected, unmodified_frame