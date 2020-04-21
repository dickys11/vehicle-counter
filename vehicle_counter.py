import cv2
<<<<<<< HEAD
import imutils
import numpy as np


cap = cv2.VideoCapture('media/video.mp4')
fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=True)
kernel_open = np.ones((11, 11), np.uint8)
kernel_close = np.ones((25, 25), np.uint8)

while(cap.isOpened()):
    _, frame = cap.read()
    fgmask = fgbg.apply(frame)

    try:
        # Apply binary threshold
        _, binFrame = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)
        # Apply opening morph
        opening = cv2.morphologyEx(binFrame, cv2.MORPH_OPEN, kernel_open)
        # Apply closing morph
        closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel_close)

        cv2.imshow('Fg Mask', closing)
    except:
        print('EOF')
        break

    contours, hierarchy = cv2.findContours(
        closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        cv2.drawContours(frame, contour, 1, (0, 0, 255), 3, 8)
        area = cv2.contourArea(contour)
        print(area)
        if area > 300:
            m = cv2.moments(contour)
            cx = int(m['m10']/m['m00'])
            cy = int(m['m01']/m['m00'])
            x, y, w, h = cv2.boundingRect(contour)
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
            img = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.imshow('Frame', frame)
=======
import numpy as np

# pilih sumber video
cap = cv2.VideoCapture('media/two lanes.mp4')
bgsub = cv2.createBackgroundSubtractorMOG2(detectShadows=True)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

# loop selama masih ada frame yang bisa dibaca
while(cap.isOpened()):
    # baca video per frame
    ret, frame = cap.read()

    # apply bgsub
    fgmask = bgsub.apply(frame)
    try:
        # apply binary trheshold
        _, binFrame = cv2.threshold(fgmask, 200, 225, cv2.THRESH_BINARY)

        # apply closing to fill small holes
        closing = cv2.morphologyEx(binFrame, cv2.MORPH_CLOSE, kernel)

        # apply opening to remove noise
        opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)

        # apply dilate
        dilation = cv2.dilate(opening, kernel, iterations=2)

    except:
        print("EOF")
        break

    # tampilkan video perframe
    cv2.imshow("frame", frame)
    cv2.imshow("final", dilation)

    # untuk keluar menggunakan esc
>>>>>>> 9868c1154203672a49cdfb0c6fcb4610e293886c
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

<<<<<<< HEAD
=======
# tutup dan hapus semua window yang terbuka
>>>>>>> 9868c1154203672a49cdfb0c6fcb4610e293886c
cap.release()
cv2.destroyAllWindows()
