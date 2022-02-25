import cv2
import keyboard
import numpy as np

def colorDetection(frame, size):
    size = str(size).split('*')
    size = int(size[0])

    rows, cols = frame.shape
    result = np.zeros((rows, cols), 'uint8')

    mask = np.ones((size, size)) / size**2

    min_y, max_y = int(rows * (2/5)), int(rows * (3/5))
    min_x, max_x =  int(cols * (2/5)), int(cols * (3/5))
    
    result = cv2.filter2D(frame, -1, mask)
    result[min_y:max_y, min_x:max_x] = frame[min_y:max_y, min_x:max_x]
    cv2.rectangle(result, (min_x, min_y), (max_x, max_y), (0, 0, 0), 2)

    height_rectangle, width_rectangle = (max_y - min_y), (max_x - min_x)
    
    black = 255 * (1/3)
    gray = 255 * (2/3)

    mask_for_color = np.ones((height_rectangle, width_rectangle)) / (height_rectangle * width_rectangle)

    result_sum = np.sum(frame[min_y:max_y, min_x:max_x] * mask_for_color)

    # result_sum = 0
    # for i in range(min_y, max_y):
    #     for j in range(min_x, max_x):
    #         result_sum += (frame[i ,j] / (height_rectangle * width_rectangle))

    if int(result_sum) < black:
        cv2.putText(result, 'Black', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    elif black < int(result_sum) < gray:
        cv2.putText(result, 'Gray', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    elif int(result_sum) > gray:
        cv2.putText(result, 'White', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    
    return result

video_cap = cv2.VideoCapture(0)

frame_width, frame_height = int(video_cap.get(3)), int(video_cap.get(4))
size = (frame_width, frame_height)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
frame_rate = 24

video_writer = cv2.VideoWriter('output.mp4', fourcc, frame_rate, size, 0)

while True:
    ret, frame = video_cap.read()
    if ret == False or keyboard.is_pressed('esc'):
        break
    
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    result = colorDetection(gray_frame, '25*25')
    video_writer.write(result)
    cv2.imshow('cam-0', result)
    cv2.waitKey(1)

video_cap.release()
video_writer.release()
cv2.destroyAllWindows()