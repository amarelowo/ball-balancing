import cv2 as cv

capture =  cv.VideoCapture(0)

while True:

    success, frame = capture.read()
    if frame is None:
        break

    cv.imshow("Camera", frame)

    key = cv.waitKey(30)
    if key == ord('q') or key == 27:
        break