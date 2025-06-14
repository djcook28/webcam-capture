import streamlit as st
import cv2
import time
import send_email
import frame_processor

st.title("Webcam Movement Capture")
start = st.button("Start")
captured_images = []

if start:
    displayed_image = st.image([])
    video = cv2.VideoCapture(0)
    stop = st.button('Stop')

    last_frame = None
    # movement_list tracks whether there was or was not movement in the last 2 frames
    movement_list = [False, False]

    while not stop:
        # movement_detected checks if there was movement in the current frame
        movement_detected = False
        check, unmodified_frame = video.read()

        # changes the image from color to greyscale reducing the frame array
        current_frame = frame_processor.simplify_frame(unmodified_frame)

        if last_frame is None:
            last_frame = current_frame

        movement_detected, unmodified_frame = frame_processor.frame_compare(last_frame, current_frame, unmodified_frame)

        if movement_detected:
            captured_images.append(current_frame)
            captured_images = captured_images[-10:]

        # append latest frame movement detection to list, only retain last 2 values
        movement_list.append(movement_detected)
        movement_list = movement_list[-2:]

        # checks if the frame before had movement and this current frame does not.  If so we want to send an email with the last frame
        if movement_list[0] == True and movement_list[1] == False:
            middle_image = captured_images[int(len(captured_images)/2)]
            cv2.imwrite('images/image.png', middle_image)
            send_email.send_email('images/image.png')
            captured_images = []

        current_datetime = time.strftime("%m/%d/%Y %H:%M:%S", time.localtime()).split(" ")

        cv2.putText(img=unmodified_frame, text=current_datetime[0], org=(50, 30), fontFace=cv2.FONT_HERSHEY_PLAIN,
                    thickness=2, fontScale=1, color=(20, 100, 20), lineType=cv2.LINE_AA)
        cv2.putText(img=unmodified_frame, text=current_datetime[1], org=(50, 50), fontFace=cv2.FONT_HERSHEY_PLAIN,
                    thickness=2, fontScale=1, color=(20, 100, 20), lineType=cv2.LINE_AA)

        displayed_image.image(unmodified_frame)

        last_frame = current_frame

        time.sleep(1)
    video.release()