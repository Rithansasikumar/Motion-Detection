import cv2
import numpy as np

# Initialize the video capture object
cap = cv2.VideoCapture(0)  # You can also use a video file by specifying its path

# Define the codec and create a VideoWriter object to save the output video
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

# Initialize variables for motion detection
prev_frame = None
threshold = 1000 # Adjust this threshold based on your environment
motion_detected = False

while True:
    ret, frame = cap.read()
    
    if not ret:
        break

    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    if prev_frame is not None:
        # Calculate the absolute difference between the current frame and the previous frame
        frame_diff = cv2.absdiff(prev_frame, gray_frame)
        
        # Apply a Gaussian blur to the difference image to reduce noise
        frame_diff = cv2.GaussianBlur(frame_diff, (5, 5), 0)
        
        # Threshold the difference image to detect motion
        _, thresh = cv2.threshold(frame_diff, 20, 255, cv2.THRESH_BINARY)
        
        # Find contours in the thresholded image
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            # If the contour area is greater than the threshold, consider it as motion
            if cv2.contourArea(contour) > threshold:
                motion_detected = True
                break

    # Draw a bounding box around the detected motion
    if motion_detected:
        cv2.putText(frame, 'Motion Detected', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.rectangle(frame, (0, 0), (640, 480), (0, 0, 255), 2)
        motion_detected = False

    # Display the frame with motion detection
    cv2.imshow('Motion Detection', frame)
    
    # Save the frame to the output video
    out.write(frame)

    prev_frame = gray_frame

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and writer objects
cap.release()
out.release()

# Close all OpenCV windows
cv2.destroyAllWindows()
