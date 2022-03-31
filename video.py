import cv2
import time

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
fourcc = cv2.VideoWriter_fourcc(*"DIVX")
videoWriter = cv2.VideoWriter("output.avi", fourcc, 5, (1280, 720), isColor=True)

dTime =  time.time()

try:
    print("Start...")
    while (True):
        ret, frame = capture.read()
        if ret:
            print(time.time()-dTime)
            dTime =  time.time()
            frame = cv2.resize(frame, (1280, 720))
            videoWriter.write(frame)

except KeyboardInterrupt:
    print("\nClose...")
finally:
    capture.release()
    videoWriter.release()
    cv2.destroyAllWindows()
