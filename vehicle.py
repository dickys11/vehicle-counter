import cv2
import numpy as np


def applyFilter(frame):
    kernelOpening = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    kernelClosing = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

    # apply closing to fill small holes
    mask = cv2.morphologyEx(frame, cv2.MORPH_CLOSE, kernelClosing)

    # apply opening to remove noise
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernelOpening)

    # apply dilate
    dilation = cv2.dilate(mask, kernelClosing, iterations=1)

    return mask


def empty(a):
    pass


cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters", 300, 40)
cv2.createTrackbar("AreaMin", "Parameters", 900, 30000, empty)


def getContours(frame, frameCopy):
    contours, _ = cv2.findContours(
        frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        area = cv2.contourArea(contour)
        areaMin = cv2.getTrackbarPos("AreaMin", "Parameters")

        if area > areaMin:
            # print(area)
            # cv2.drawContours(frameCopy, contour, -1, (0, 255, 0), 2, 8)
            M = cv2.moments(contour)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frameCopy, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.circle(frameCopy, (cx, cy), 5, (0, 0, 255), -1)


# pilih sumber video
cap = cv2.VideoCapture('media/two lanes.mp4')
bgsub = cv2.createBackgroundSubtractorKNN(detectShadows=False)


# loop selama masih ada frame yang bisa dibaca
while(cap.isOpened()):
    # baca video per frame
    ret, frame = cap.read()
    frameCopy = frame.copy()
    # mask = frame.copy()
    if not ret:
        print('EOF')
        break

    # apply bgsub
    fgmask = bgsub.apply(frame)
    mask = applyFilter(fgmask)
    getContours(mask, frameCopy)

    # tampilkan video perframe
    cv2.imshow("frame", frameCopy)
    cv2.imshow("mask", mask)

    # untuk keluar menggunakan esc
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

# tutup dan hapus semua window yang terbuka
cap.release()
cv2.destroyAllWindows()
