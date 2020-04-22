import cv2
import imutils
import numpy as np


cap = cv2.VideoCapture('media/two lanes.mp4')
fgbg = cv2.createBackgroundSubtractorKNN(detectShadows=True)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

while(cap.isOpened()):
    _, frame = cap.read()
    fgmask = fgbg.apply(frame)

    # Apply binary threshold
    _, binFrame = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)
    # Apply closing morph
    mask = cv2.morphologyEx(binFrame, cv2.MORPH_CLOSE, kernel)
    # Apply opening morph
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    # Apply dilate
    dilation = cv2.dilate(mask, kernel, iterations=2)
    cv2.imshow('Fg Mask', mask)

    contours, hierarchy = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        #cv2.drawContours(frame, cnt, -1, (0, 255, 0), 3, 8)
        area = cv2.contourArea(cnt)
        # print(area)
        if area > 500:
            M = cv2.moments(cnt)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
            img = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.imshow('Frame', frame)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
