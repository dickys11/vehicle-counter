import cv2
import numpy as np

cap = cv2.VideoCapture('media/beachfront.mp4')

while(cap.isOpened()):
    ret, frame = cap.read()

    cv2.imshow("frame", frame)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
