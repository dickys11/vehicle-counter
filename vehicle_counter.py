import cv2
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
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

# tutup dan hapus semua window yang terbuka
cap.release()
cv2.destroyAllWindows()
