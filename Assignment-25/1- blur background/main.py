import cv2
import numpy as np

img = cv2.imread('flower_input.jpg', 0)
rows, cols = img.shape
result = np.zeros((rows, cols), 'uint8')

ret, thresh = cv2.threshold(img, 180, 255, cv2.THRESH_BINARY)
mask = np.ones((25, 25)) / 625

for i in range(12, rows-12):
    for j in range(12, cols-12):
        if thresh[i, j] != 255:
            small_img = img[i-12:i+13, j-12:j+13]
            result[i ,j] = np.sum(small_img * mask)
        else:
            result[i, j] = img[i, j]

cv2.imshow('result', result)
cv2.imwrite('result.jpg', result)
cv2.waitKey()