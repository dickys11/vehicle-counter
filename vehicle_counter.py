import cv2
import numpy as np

# pilih sumber video
cap = cv2.VideoCapture('media/beachfront.mp4')
bgsub = cv2.createBackgroundSubtractorMOG2(detectShadows=True)
kernel = np.ones((5, 5), np.uint8)

# loop selama masih ada frame yang bisa dibaca
while(cap.isOpened()):
    # baca video per frame
    ret, frame = cap.read()
    # apply bgsub
    fgmask = bgsub.apply(frame)
    # apply binary trheshold
    _, binFrame = cv2.threshold(fgmask, 200, 225, cv2.THRESH_BINARY)

    # tampilkan video perframe
    cv2.imshow("frame", frame)
    cv2.imshow("mask", fgmask)
    cv2.imshow("binary masked", binFrame)

    # untuk keluar menggunakan esc
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

# tutup dan hapus semua window yang terbuka
cap.release()
cv2.destroyAllWindows()
