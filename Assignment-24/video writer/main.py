import cv2
import keyboard

video_cap = cv2.VideoCapture(0)

frame_width, frame_height = int(video_cap.get(3)), int(video_cap.get(4))
size = (frame_width, frame_height)
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
frame_rate = 24

video_writer = cv2.VideoWriter('output.mp4', fourcc, frame_rate, size)

while True:
    ret, frame = video_cap.read()
    if not ret:
        break
    if keyboard.is_pressed('esc'):
        break
    
    video_writer.write(frame)
    cv2.imshow('cam', frame)
    cv2.waitKey(1)

video_cap.release()
video_writer.release()
cv2.destroyAllWindows()