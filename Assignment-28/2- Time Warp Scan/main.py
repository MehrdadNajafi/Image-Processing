import cv2
import keyboard
import numpy as np

class GreenLine:
    def __init__(self, y):
        self.y = y
        self.speed = 1
        self.color = (0, 255, 0)
    
    def move(self):
        self.y += self.speed

video_cap = cv2.VideoCapture(0)

frame_width, frame_height = int(video_cap.get(3)), int(video_cap.get(4))
size = (frame_width, frame_height)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
frame_rate = 20

video_writer = cv2.VideoWriter('output.mp4', fourcc, frame_rate, size)

rows, cols = frame_height, frame_width

result = np.zeros((rows, cols, 3), dtype='uint8')

line = GreenLine(0)


while line.y < rows:
    ret, frame = video_cap.read()
    if not ret or keyboard.is_pressed('esc'):
        break
    
    for i in range(rows):
        if line.y-1 == i:
            result[i, :] = frame[i, :]
        elif i >= line.y:
            result[i, :] = frame[i, :]
            
    result[line.y:line.y+2, :] = line.color
            
    line.move()
    cv2.imshow('', result)
    video_writer.write(result)
    cv2.waitKey(1)
    
cv2.imwrite('output.jpg', result)

video_cap.release()
video_writer.release()
cv2.destroyAllWindows()