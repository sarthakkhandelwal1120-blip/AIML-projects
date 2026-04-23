import cv2
import numpy as np
import time

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera not working")
    exit()

# Read first frames safely
ret, frame1 = cap.read()
ret, frame2 = cap.read()

print("Press 'q' to exit cleanly")

try:
    while True:
        if not ret:
            break

        # Frame difference
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5,5), 0)

        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)

        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        motion_detected = False

        for contour in contours:
            if cv2.contourArea(contour) < 2000:
                continue

            motion_detected = True
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame1, (x,y), (x+w,y+h), (0,255,0), 2)

        if motion_detected:
            cv2.putText(frame1, "MOTION DETECTED!", (20,50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)

        cv2.imshow("Security Camera", frame1)

        # Update frames
        frame1 = frame2
        ret, frame2 = cap.read()

        # Proper exit key
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("\nProgram stopped manually")

finally:
    # ALWAYS release resources
    cap.release()
    cv2.destroyAllWindows()
    print("Camera closed properly ✅")