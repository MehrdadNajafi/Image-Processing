import cv2
import keyboard
import imutils
from imutils.perspective import four_point_transform

video_cap = cv2.VideoCapture(0)

frame_width, frame_height = int(video_cap.get(3)), int(video_cap.get(4))
size = (frame_width, frame_height)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
frame_rate = 20

video_writer = cv2.VideoWriter('output\output.mp4', fourcc, frame_rate, size)

while True:
    ret, frame = video_cap.read()
    
    if not ret or keyboard.is_pressed('esc'):
        break
    
    cv2.putText(frame, "Press 's' for crop the Sudoku", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv2.putText(frame, "Press 'ESC' for exit", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    
    original_frame = frame.copy()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_blurred = cv2.GaussianBlur(gray_frame, (5, 5), 3)

    thresh = cv2.adaptiveThreshold(frame_blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    thresh = 255 - thresh

    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # contours = contours[0]

    contours = imutils.grab_contours(contours)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    sudoku_contour = None
    
    for contour in contours:
        epsilon = 0.12 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        if len(approx) == 4:
            sudoku_contour = approx
            break
    
    if sudoku_contour is None or (sudoku_contour is None and keyboard.is_pressed('s')):
        print("Can't find any Sudoku in this frame")
    else:
        cv2.drawContours(frame, [sudoku_contour], -1, (0, 255, 0), 10)
        if keyboard.is_pressed('s'):
            warped = four_point_transform(original_frame, sudoku_contour.reshape(4, 2))
            cv2.imwrite('output\sudoku from frame.jpg', warped)
    
    cv2.imshow('Cam-0', frame)
    video_writer.write(frame)
    cv2.waitKey(1)
    
video_cap.release()
video_writer.release()
cv2.destroyAllWindows()