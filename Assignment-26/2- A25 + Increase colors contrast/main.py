import cv2
import keyboard
import numpy as np
import matplotlib.pyplot as pt


def automatic_brightness_and_contrast(image, clip_hist_percent=1):
    gray = image
    
    # Calculate grayscale histogram
    hist = cv2.calcHist([gray],[0],None,[256],[0,256])
    hist_size = len(hist)
    
    # Calculate cumulative distribution from the histogram
    accumulator = []
    accumulator.append(float(hist[0]))
    for index in range(1, hist_size):
        accumulator.append(accumulator[index -1] + float(hist[index]))
    
    # Locate points to clip
    maximum = accumulator[-1]
    clip_hist_percent *= (maximum/100.0)
    clip_hist_percent /= 2.0
    
    # Locate left cut
    minimum_gray = 0
    while accumulator[minimum_gray] < clip_hist_percent:
        minimum_gray += 1
    
    # Locate right cut
    maximum_gray = hist_size -1
    while accumulator[maximum_gray] >= (maximum - clip_hist_percent):
        maximum_gray -= 1
    
    # Calculate alpha and beta values
    alpha = 255 / (maximum_gray - minimum_gray)
    beta = -minimum_gray * alpha
    
    '''
    # Calculate new histogram with desired range and show histogram 
    new_hist = cv2.calcHist([gray],[0],None,[256],[minimum_gray,maximum_gray])
    plt.plot(hist)
    plt.plot(new_hist)
    plt.xlim([0,256])
    plt.show()
    '''

    auto_result = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return (auto_result, alpha, beta)

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
    
    # result[min_y:max_y, min_x:max_x] = cv2.equalizeHist(result[min_y:max_y, min_x:max_x])

    height_rectangle, width_rectangle = (max_y - min_y), (max_x - min_x)
    
    black = 255 * (1/3)
    gray = 255 * (2/3)

    mask_for_color = np.ones((height_rectangle, width_rectangle)) / (height_rectangle * width_rectangle)

    result_sum = np.sum(frame[min_y:max_y, min_x:max_x] * mask_for_color)
    
    # 1
    # result[min_y:max_y, min_x:max_x], alpha, beta = automatic_brightness_and_contrast(result[min_y:max_y, min_x:max_x])
    
    # 2
    # result[min_y:max_y, min_x:max_x] = cv2.normalize(result[min_y:max_y, min_x:max_x], None, 0, 255, cv2.NORM_MINMAX)
    
    # 3
    # clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    # result[min_y:max_y, min_x:max_x] = clahe.apply(result[min_y:max_y, min_x:max_x])

    # 4
    alpha = 2 # Contrast control (1.0-3.0)
    beta = 0 # Brightness control (0-100)
    result[min_y:max_y, min_x:max_x] = cv2.convertScaleAbs(result[min_y:max_y, min_x:max_x], alpha=alpha, beta=beta)

    # result_sum = 0
    # for i in range(min_y, max_y):
    #     for j in range(min_x, max_x):
    #         result_sum += (frame[i ,j] / (height_rectangle * width_rectangle))
    
    cv2.putText(result, f'average of colors: {int(result_sum)}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 2)

    if int(result_sum) < black:
        cv2.putText(result, 'Black', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    elif black < int(result_sum) < gray:
        cv2.putText(result, 'Gray', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    elif int(result_sum) > gray:
        cv2.putText(result, 'White', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    
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