import cv2
import numpy as np


cap = cv2.VideoCapture(0)  


fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

prev_frame = None
threshold = 1000 # Adjust this threshold
motion_detected = False

while True:
    ret, frame = cap.read()
    
    if not ret:
        break

    
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    if prev_frame is not None:
        frame_diff = cv2.absdiff(prev_frame, gray_frame)
        
        frame_diff = cv2.GaussianBlur(frame_diff, (5, 5), 0)
        
        _, thresh = cv2.threshold(frame_diff, 20, 255, cv2.THRESH_BINARY)
        
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            if cv2.contourArea(contour) > threshold:
                motion_detected = True
                break

    
    if motion_detected:
        cv2.putText(frame, 'Motion Detected', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.rectangle(frame, (0, 0), (640, 480), (0, 0, 255), 2)
        motion_detected = False

    
    cv2.imshow('Motion Detection', frame)
    
    out.write(frame)

    prev_frame = gray_frame

    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()


cv2.destroyAllWindows()
