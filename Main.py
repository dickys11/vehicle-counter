import cv2
import numpy as np
import Car

# Set Variable
point1 = (0, 0)
point2 = (0, 0)
lineUp = 0
lineDown = 0
upLimit = 0
downLimit = 0
topClicked = False
bottomClicked = False
font = cv2.FONT_HERSHEY_SIMPLEX
cars = []
max_p_age = 5
pid = 1
counterUp = 0
counterDown = 0


# Function to draw rectangle with mouse
def drawRectangle(event, x, y, flags, param):
    # call variable
    global point1, point2, topClicked, bottomClicked

    # left mouse click
    if event == cv2.EVENT_LBUTTONDOWN:
        # get top left coordinates
        if not topClicked:
            point1 = (x, y)
            topClicked = True
        # get bottom right coordinates
        elif not bottomClicked:
            point2 = (x, y)
            bottomClicked = True


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


def count(mask, frame):
    global areaTH, cars, pt1, pt2, upLimit, downLimit, lineUp, lineDown, counterDown, counterUp, pid, max_p_age

    contours, _ = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > areaTH:
            M = cv2.moments(cnt)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            x, y, w, h = cv2.boundingRect(cnt)

            newCar = True
            if cy in range(upLimit, downLimit):
                for i in cars:
                    if abs(cx - i.getX()) <= w and abs(cy - i.getY() <= h):
                        newCar = False
                        i.updateCoords(cx, cy)
                        if i.going_UP(lineDown, lineUp) == True:
                            counterUp += 1
                        elif i.going_DOWN(lineDown, lineUp) == True:
                            counterDown += 1
                        break
                    if i.getState() == '1':
                        if i.getDir() == 'down' and i.getY() > downLimit:
                            i.setDone()
                        elif i.getDir() == 'up' and i.getY() < downLimit:
                            i.setDone()
                    if i.timedOut():
                        index = cars.index(i)
                        cars.pop(index)
                        del i
                if newCar == True:
                    p = Car.MyCar(pid, cx, cy, max_p_age)
                    cars.append(p)
                    pid += 1
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    for i in cars:
        cv2.putText(frame, str(i.getId()), (i.getX(), i.getY()),
                    font, 0.3, i.getRGB(), 1, cv2.LINE_AA)


cap = cv2.VideoCapture('media/source.mp4')
w = int(cap.get(3))
h = int(cap.get(4))
areaTH = (w*h)/750
bgsub = cv2.createBackgroundSubtractorKNN()


cv2.namedWindow('Main')
cv2.setMouseCallback('Main', drawRectangle)

firstFrame = True

while cap.isOpened():
    ret, frame = cap.read()

    for i in cars:
        i.age_one()

    fgmask = bgsub.apply(frame)
    mask = applyFilter(fgmask)
    count(mask, frame)

    while firstFrame:
        cv2.imshow('Main', frame)
        upLimit = point1[1]
        if topClicked:
            cv2.line(frame, (0, upLimit),
                     (w, upLimit), (255, 255, 255), 2)
        downLimit = point2[1]
        if bottomClicked:
            cv2.line(frame, (0, downLimit),
                     (w, downLimit), (255, 255, 255), 2)
        delta = (downLimit - upLimit)/3
        lineUp = int(upLimit + delta)
        lineDown = int(downLimit - delta)
        if cv2.waitKey(1) & 0xFF == ord('c'):
            firstFrame = False
            break

    if topClicked and bottomClicked:
        str_up = 'UP: ' + str(counterUp)
        str_down = 'DOWN: ' + str(counterDown)
        cv2.putText(frame, str_up, (10, 40), font, 0.5,
                    (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, str_up, (10, 40), font,
                    0.5, (0, 0, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, str_down, (10, 90), font,
                    0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, str_down, (10, 90), font,
                    0.5, (255, 0, 0), 1, cv2.LINE_AA)

        cv2.line(frame, (0, upLimit),
                 (w, upLimit), (255, 255, 255), 2)
        cv2.line(frame, (0, lineDown),
                 (w, lineDown), (255, 255, 255), 2)
        cv2.line(frame, (0, lineUp),
                 (w, lineUp), (255, 255, 255), 2)
        cv2.line(frame, (0, downLimit),
                 (w, downLimit), (255, 255, 255), 2)

    cv2.imshow('Main', frame)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
