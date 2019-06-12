import cv2
import json

def imageCapture():
    video_capture = cv2.VideoCapture(False)
    if not video_capture.isOpened():
        raise Exception("Could not open video device")
    ret, frame = video_capture.read()
    print(type(frame))
    #with open('image_file.txt', 'w') as outfile:
    #    outfile.write(str(frame))
    video_capture.release()



imageCapture()
