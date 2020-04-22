import cv2
import numpy as np


def empty(a):
    pass


cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters", 640, 240)
cv2.createTrackbar("Area", "Parameters", 5000, 30000, empty)


def getContours(img, imgContour):
    contours, hierarchy = cv2.findContours(
        img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        areaMin = cv2.getTrackbarPos("Area", "Parameters")
        if area > areaMin:
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 255), 7)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            # print(len(approx))
            x, y, w, h = cv2.boundingRect(approx)
            cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 5)

            cv2.putText(imgContour, "Points: " + str(len(approx)), (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX, .7,
                        (0, 255, 0), 2)
            cv2.putText(imgContour, "Area: " + str(int(area)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                        (0, 255, 0), 2)


# pilih sumber video
cap = cv2.VideoCapture('media/source.mp4')
bgsub = cv2.createBackgroundSubtractorMOG2(detectShadows=False)
kernelOp = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
kernelCl = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

# loop selama masih ada frame yang bisa dibaca
while(cap.isOpened()):
    # baca video per frame
    ret, frame = cap.read()
    imgContour = frame.copy()
    if frame is None:
        print('error')
        break

    # apply bgsub
    fgmask = bgsub.apply(frame)

    # apply binary trheshold
    _, binFrame = cv2.threshold(fgmask, 200, 225, cv2.THRESH_BINARY)

    # apply closing to fill small holes
    closing = cv2.morphologyEx(binFrame, cv2.MORPH_CLOSE, kernelOp)

    # apply opening to remove noise
    opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernelCl)

    # apply dilate
    dilation = cv2.dilate(opening, kernelOp, iterations=2)

    getContours(dilation, imgContour)

    # tampilkan video perframe
    cv2.imshow("frame", frame)
    cv2.imshow("final", imgContour)

    # untuk keluar menggunakan esc
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

# tutup dan hapus semua window yang terbuka
cap.release()
cv2.destroyAllWindows()
