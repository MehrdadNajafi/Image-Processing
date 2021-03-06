import cv2
import numpy as np

img = cv2.imread('lion.png', 0)
rows, cols = img.shape
result = np.zeros((rows, cols), 'uint8')

mask = [[0, -1, 0],
        [-1, 4, -1],
        [0, -1, 0]]

for i in range(1, rows-1):
    for j in range(1, cols-1):
        small_img = img[i-1:i+2, j-1:j+2]
        result[i, j] = np.sum(small_img * mask)

cv2.imwrite('result.jpg', result)
cv2.imshow('', result)
cv2.waitKey()