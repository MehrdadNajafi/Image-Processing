import cv2
import keyboard
import numpy as np

def skin_Detection(frame):
    frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    lower = np.array([0, 45, 58], dtype = "uint8")
    upper = np.array([20, 150, 250], dtype = "uint8")

    lower2 = np.array([172, 45, 58], dtype = "uint8")
    upper2 = np.array([179, 150, 250], dtype = "uint8")
    
    skinMask = cv2.inRange(frame_HSV, lower, upper)
    skinMask2 = cv2.inRange(frame_HSV, lower2, upper2)
    
    skinMask = cv2.GaussianBlur(skinMask, (3, 3), 0)
    skinMask2 = cv2.GaussianBlur(skinMask2, (3, 3), 0)
    
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 8))
    hsv_d = cv2.dilate(skinMask, kernel)
    hsv_d_2 = cv2.dilate(skinMask2, kernel)
    
    skin1 = cv2.bitwise_and(frame, frame, mask = hsv_d)
    skin2 = cv2.bitwise_and(frame, frame, mask = hsv_d_2)
    skin = cv2.bitwise_or(skin1,skin2) #adding both ranges
    
    return skin

video_cap = cv2.VideoCapture(0)

frame_width, frame_height = int(video_cap.get(3)), int(video_cap.get(4))
size = (frame_width, frame_height)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
frame_rate = 20

video_writer = cv2.VideoWriter('output.mp4', fourcc, frame_rate, size)

while True:
    ret, frame = video_cap.read()
    if not ret or keyboard.is_pressed('esc'):
        break
    
    frame_result = skin_Detection(frame)
    
    video_writer.write(frame_result)
    cv2.imshow('Cam-0', frame_result)
    cv2.waitKey(1)
    
video_writer.release()
video_cap.release()
cv2.destroyAllWindows()